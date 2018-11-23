import javax.net.ssl.HttpsURLConnection;
import java.io.*;
import java.math.BigInteger;
import java.net.URL;
import java.security.cert.Certificate;
import java.security.interfaces.RSAKey;
import java.util.*;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.logging.Logger;

/**
 * consider that because of IOException, the data write to file may be not complete
 * (specially, the line may not contain a legal number( or a legal modulus number) or may not contain a legal text)
 * however, for this task, this is not very important,
 * and u can check whether the modulus is of 2's pow's len(i.e 1024, 2048, 4096)
 */
class GetModulus {

    public static void main(String[] argv) throws IOException, InterruptedException {
        getModulusFromUrlDir("./src/all.properties");
        getModulusUseRandomIP(1 << 14, "./modulusDBSDir_IP", "./modulusDir_IP");
    }

    public static void getModulusFromUrlDir(String propertyFile) throws IOException, InterruptedException {
        Properties properties = new Properties();
        properties.load(new FileReader(propertyFile));
        getModulusFromUrlDir(properties.getProperty("SrcUrlFileDir"),
                properties.getProperty("DestModulusFileDir"),
                properties.getProperty("DestModulusDBDir"),
                1024, 8, 10000);
    }

    public static void getModulusUseRandomIP(int attemptCnt, String modulusDBDir, String modulusDir) throws IOException, InterruptedException {
        {
            File s = new File(modulusDBDir);
            if (!s.exists() && !s.mkdir()) {
                throw new IOException("can't create the modulusDBDir");
            }
            File s1 = new File(modulusDir);
            if (!s1.exists() && !s1.mkdir()) {
                throw new IOException("can't create the modulusDBDir");
            }
        }
        final int maxEverySetCnt = 1024;
        ExecutorService pool = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        for (int i = 0; i < attemptCnt; i++) {
            int finalI = i;
            pool.submit(() -> {
                HashSet<String> ipSet = new HashSet<>();
                try {
                    while (ipSet.size() < maxEverySetCnt) {
                        String ip = "https://" + (int) (Math.random() * 256) + "." + (int) (Math.random() * 256) + "." + (int) (Math.random() * 256) + "." + (int) (Math.random() * 256);
                        Logger.getGlobal().info(ip);
                        ipSet.add(ip);
                    }
                    getModulusFromUrlOrIpList(ipSet, modulusDir + "/" + finalI, modulusDBDir + "/" + finalI, 1024, 10000);
                } catch (Throwable e) {
                    e.printStackTrace();
                    System.exit(1);
                }
                Logger.getGlobal().info("get " + ipSet.size() + " ip finish");
            });
        }
        pool.shutdown();
        pool.awaitTermination(1000, TimeUnit.DAYS);
    }


    /**
     * @param urlFileDir        the dir where there are some files, every files have several lines, each line is a url (begin with https://)
     * @param modulusFileDir    the dir where to store the modulus, each urlFile's modulus is store in one modulus file
     * @param modulusDBDir      the dir where every file store the a <code>HashMap<BigInteger, HashSet<String>></code> object(the key is modulus, the value is url set)
     *                          every url file corresponding to one file
     * @param threadCntEachFile this method call <code>getModulusFromUrlFile</code>
     * @param threadCntEachDir  every file will be a task(call a method that get modulus for a file) to submit to the threadPool,
     *                          so this param spec the threadCnt for this pool
     * @param timeOut           is set for the socket( of millisecond ), all threadPool's timeOut is 1000 Days
     */
    private static void getModulusFromUrlDir(String urlFileDir, String modulusFileDir, String modulusDBDir,
                                            int threadCntEachFile, int threadCntEachDir, int timeOut)
            throws IOException, InterruptedException {
        {
            var tmp = new File(modulusDBDir);
            if (!tmp.exists() && !tmp.mkdir()) {
                throw new IOException("can't not create " + modulusDBDir);
            }
            tmp = new File(modulusFileDir);
            if (!tmp.exists() && !tmp.mkdir()) {
                throw new IOException("can't not create " + modulusDBDir);
            }
        }
        File urlDir = new File(urlFileDir);
        File[] files = urlDir.listFiles();
        Objects.requireNonNull(files);
        ExecutorService pool = Executors.newFixedThreadPool(threadCntEachDir);
        for (int i = 0; i < files.length; i++) {
            if (!files[i].isFile()) {
                continue;
            }
            final int finalI = i;
            pool.submit(() -> {
                try {
                    getModulusFromUrlFile(files[finalI].toString(), modulusFileDir + finalI,
                            modulusDBDir + finalI, threadCntEachFile, timeOut);
                } catch (IOException | InterruptedException e) {
                    e.printStackTrace();
                }
            });
        }
        pool.shutdown();
        pool.awaitTermination(1000, TimeUnit.DAYS);
    }

    private static void getModulusFromUrlFile(String urlFilePath, String modulusFilePath, String modulusDBPath,
                                              int threadCnt, int timeOut) throws IOException, InterruptedException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(urlFilePath)));
        String r;
        ArrayList<String> rs = new ArrayList<>();
        while ((r = reader.readLine()) != null) {
            rs.add(r);
        }
        getModulusFromUrlOrIpList(rs, modulusFilePath, modulusDBPath, threadCnt, timeOut);
    }


    /**
     * @param modulusFilePath the modulus get from the urlOrIpList will all store in this file, one line one modulus
     * @param modulusDBPath   the <code>HashMap<BigInteger, HashSet<String>></code> object(the key is modulus, the value is url set)
     * @param timeOut         for that some url will make too long to visit, so we need timeOut
     *                        consider that, because of IOException, the process that write to file a line will be interrupted, so the line is not very reliable
     */
    private static void getModulusFromUrlOrIpList(Collection<String> urlOrIpList, final String modulusFilePath, String modulusDBPath,
                                                  int threadCnt, int timeOut)
            throws IOException, InterruptedException {
        final ExecutorService pool = Executors.newFixedThreadPool(threadCnt);
        final ConcurrentLinkedQueue<BigInteger> writeQue = new ConcurrentLinkedQueue<>();
        final AtomicInteger progress = new AtomicInteger(0);
        final Thread writeToFile = new Thread(() -> {
            try (FileWriter modulus = new FileWriter(modulusFilePath)) {
                final int everyTimeWrite = 20;
                while (true) {
                    for (int i = 0; i < everyTimeWrite; i++) {
                        if (!writeQue.isEmpty()) {
                            // this method can not make sure that all str pass to it will be writen
                            // it may write a part of it
                            // i just make all the write to file thread end when exception occurred
                            modulus.write(writeQue.poll().toString() + "\n");
                        } else {
                            if (Thread.interrupted()) {
                                modulus.close();
                                return;
                            }
                            modulus.flush();
                            Thread.yield();
                        }
                    }
                    modulus.flush();
                }
            } catch (IOException e) { // the exception is catch by File
                e.printStackTrace();
                for (var i : e.getSuppressed()) {
                    i.printStackTrace();
                }
            }
        });
        writeToFile.start();
        // should not useConcurrentHashMap, for that i need to get the arrayList and then put to it
        var modulusToDomain = new HashMap<BigInteger, HashSet<String>>();
        for (var i : urlOrIpList) {
            pool.submit(() -> {
                Logger.getGlobal().info("begin to visit " + i);
                HashSet<BigInteger> s = visitUrlAndReturnModulus(i, timeOut);
                if (s != null && !s.isEmpty()) {
                    writeQue.addAll(s);
                    // ConcurrentHashMap don't work here
                    // for that i need to get the list and add to it
                    // so the add action is separate to several action
                    synchronized (modulusToDomain) {
                        for (var k : s) {
                            if (modulusToDomain.containsKey(k)) {
                                modulusToDomain.get(k).add(i);
                            } else {
                                var t = new HashSet<String>();
                                t.add(i);
                                modulusToDomain.put(k, t);
                            }
                        }
                    }
                }
                progress.incrementAndGet();
                Logger.getGlobal().info("progress: " + progress.toString());
            });
        }
        pool.shutdown();
        boolean isEnd = pool.awaitTermination(1000, TimeUnit.DAYS);
        Logger.getGlobal().info(isEnd ? "all urls visit finish" : "pool timeout");
        writeToFile.interrupt();
        try (FileOutputStream modulusDB = new FileOutputStream(modulusDBPath)) {
            synchronized (modulusToDomain) {
                new ObjectOutputStream(modulusDB).writeObject(modulusToDomain);
            }
        }
        Logger.getGlobal().info("write to DB finished");
    }

    /**
     * @param timeOut the timeOut of visit a url (int millisecond)
     * @return if failed return null
     * for that use an API whose returned value may not be a valid certificate chain and should not be relied on for trust decisions
     * so the modulus is not relied
     */
    private static HashSet<BigInteger> visitUrlAndReturnModulus(String url, int timeOut) {
        Certificate[] certs;
        try {
            var connection = (HttpsURLConnection) new URL(url).openConnection();
//            connection.setConnectTimeout(timeOut);
            connection.setConnectTimeout(timeOut);
            connection.setReadTimeout(timeOut);
            try {
                assert connection.getReadTimeout() == timeOut;
                assert connection.getConnectTimeout() == timeOut;
            } catch (AssertionError e) {
                e.printStackTrace();
                System.exit(1);
            }
            connection.setRequestMethod("HEAD");
            {
                long begin = System.currentTimeMillis();
                connection.connect();
                Logger.getGlobal().info(url + " use time: " + (System.currentTimeMillis() - begin));
            }
            certs = connection.getServerCertificates();
            Logger.getGlobal().info(url + ": connect success");
        } catch (IOException e) {
            Logger.getGlobal().info("visit " + url + " failed");
            return null;
        }
        HashSet<BigInteger> res = new HashSet<>();
        for (Certificate cert : certs) {
            try {
                String alg = cert.getPublicKey().getAlgorithm();
                if (!alg.equals("RSA")) {
                    Logger.getGlobal().info(url + ": One Key is not RSA, it is " + alg);
                    continue;
                }
                res.add(((RSAKey) cert.getPublicKey()).getModulus());
            } catch (ClassCastException e) {
                Logger.getGlobal().info(url + ": One Key can't cast to RSAKey");
            }
        }
        return res;
    }
}
