import HZeXLibs.util.Misc;

import java.io.*;
import java.math.BigInteger;
import java.util.*;
import java.util.logging.Logger;

public class TryToFactorModulus {
    public static void main(String[] argv) throws IOException {
        tryToCalFactor("./src/all.properties");
        findTheModulusBeFactored("./src/all.properties");
    }

    public static void findTheModulusBeFactored(String propertyFile) throws IOException {
        Properties properties = new Properties();
        properties.load(new FileReader(propertyFile));
        HashSet<BigInteger> allModulus = getModulusFromDir(properties.getProperty("DestModulusFileDir"));
        ArrayList<BigInteger> allFactor = new ArrayList<>();
        try (BufferedReader factors = new BufferedReader(new FileReader(properties.getProperty("FactorFile")))) {
            String s;
            while ((s = factors.readLine()) != null) {
                var n = new BigInteger(s);
                if (!n.isProbablePrime(100)) {
                    continue;
                }
                allFactor.add(n);
            }
        }
        HashMap<BigInteger, ArrayList<BigInteger>> factorToModulus = new HashMap<>();
        // TODO, concurrent it
        for (BigInteger factor : allFactor) {
            for (var j : allModulus) {
                if (j.divideAndRemainder(factor)[1].equals(BigInteger.ZERO)) {
                    if (!factorToModulus.containsKey(factor)) {
                        var s = new ArrayList<BigInteger>();
                        s.add(j);
                        factorToModulus.put(factor, s);
                    } else {
                        factorToModulus.get(factor).add(j);
                    }
                }
            }
        }
        try (ObjectOutputStream f2m = new ObjectOutputStream(new FileOutputStream(properties.getProperty("FactorToModulusDB")))) {
            f2m.writeObject(factorToModulus);
        }
    }

    public static void tryToCalFactor(String propertyFile) throws IOException {
        Properties properties = new Properties();
        properties.load(new FileReader(propertyFile));
        HashSet<BigInteger> allModulus = getModulusFromDir(properties.getProperty("DestModulusFileDir"));
        Logger.getGlobal().info("there are " + allModulus.size() + " modulus");
        int t = Misc.ceilTo2Pow(allModulus.size());
        BigInteger[] modulusList = new BigInteger[t];
        {
            int j = 0;
            for (var i : allModulus) {
                modulusList[j++] = i;
            }
        }
        for (int i = allModulus.size(); i < t; i++) {
            modulusList[i] = BigInteger.valueOf(1);
        }
        var gcd = new ParallelBatchGCD().worker(modulusList);
        try (FileOutputStream factors = new FileOutputStream(properties.getProperty("FactorFile"))) {
            for (BigInteger aGcd : gcd) {
                if (!aGcd.equals(BigInteger.ONE) && aGcd.isProbablePrime(100)) {
                    factors.write((aGcd.toString() + "\n").getBytes());
                }
            }
        }
    }

    private static HashSet<BigInteger> getModulusFromDir(String modulusDirPath) throws IOException {
        File[] mf = new File(modulusDirPath).listFiles();
        Objects.requireNonNull(mf);
        HashSet<BigInteger> allModulus = new HashSet<>();
        int allLine = 0;
        for (var i : mf) {
            var input = new BufferedReader(new FileReader(i));
            String s;
            while ((s = input.readLine()) != null) {
                allLine += 1;
                try {
                    allModulus.add(new BigInteger(s));
                } catch (Exception e) {
                    System.out.println(s + " " + i);
                    System.exit(0);
                }
            }
        }
        Logger.getGlobal().info("there are " + allLine + " lines");
        return allModulus;
    }

}
