import HZeXLibs.util.Misc;

import java.io.FileWriter;
import java.io.IOException;
import java.math.BigInteger;
import java.util.Arrays;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

public class TestParallelBatchGCD {
//    public

    public static void test_2() {
        final int cnt = 8;
        BigInteger[] k = new BigInteger[cnt];
        for (int i = 0; i < cnt; i++) {
            while (true) {
                BigInteger t = BigInteger.valueOf((int) (Math.random() * 1000));
                if (t.isProbablePrime(100)) {
                    k[i] = t;
                    break;
                }
            }
        }
        BigInteger[] ss = new BigInteger[cnt * cnt];
        for (int i = 0; i < cnt; i++) {
            for (int j = 0; j < cnt; j++) {
                ss[i * cnt + j] = k[i].multiply(k[j]);
            }
        }
        var t = new ParallelBatchGCD().worker(k);
        System.out.println(Arrays.toString(t));
        for (var aR : t) {
            if (!aR.equals(BigInteger.ONE)) {
                System.out.println(aR + " " + aR.isProbablePrime(100));
            }
        }
    }

    public static void test() {
        var t = new ParallelBatchGCD();
        while (true) {
            // BigInteger[] nums = new BigInteger[]{new BigInteger("100"), new BigInteger("200"), new BigInteger("300"), new BigInteger("400"), new BigInteger("100"), new BigInteger("200"), new BigInteger("300"), new BigInteger("400"), new BigInteger("100"), new BigInteger("200"), new BigInteger("300"), new BigInteger("400"), new BigInteger("100"), new BigInteger("200"), new BigInteger("300"), new BigInteger("400")};
            int cnt = 1024 * 16 * 16;
            BigInteger[] nums = new BigInteger[cnt];
            for (int i = 0; i < cnt; i++) {
                nums[i] = BigInteger.valueOf((int) (Math.random() * 10000L) + 10000L);
            }
            var r = t.productTree(nums);
            int s = r.length - 1;
//            BigInteger all;
//            BigInteger half_1 = new BigInteger("1");
//            BigInteger half_2 = new BigInteger("1");
//            System.out.println("trivial check begin: ");
//            for (int i = 0; i < nums.length / 2; i++) {
//                half_1 = half_1.multiply(nums[i]);
//            }
//            for (int i = nums.length / 2; i < nums.length; i++) {
//                half_2 = half_2.multiply(nums[i]);
//            }
//            System.out.println("trivial check end");
//            all = half_1.multiply(half_2);
//            if (r.length == 1) {
//                assert r[0].length == 1 && r[0][0].equals(nums[0]);
//            } else {
//                assert all.equals(r[s][0]) && half_1.equals(r[s - 1][0]) && half_2.equals(r[s - 1][1]) : (half_1 + " " + half_2 + " " + r[s - 2][0] + " " + r[s - 2][1] + " " + r[s - 1][0] + " " + all);
//            }
            long start1 = System.nanoTime();
            var r2 = t.remainderTree(r);
            long end1 = System.nanoTime();

            var ans = trivialGCD(nums);
            long end3 = System.nanoTime();
            Logger.getGlobal().info(String.format("%d, %d, %f", end1 - start1, end3 - end1, (double) (end3 - end1) / (end1 - start1)));

//            Logger.getGlobal().info("remainderTree end, trivial check begin");
//            final int ss = Runtime.getRuntime().availableProcessors();
//            if (nums.length < ss) {
//                for (int i = 0; i < r2.length; i++) {
//                    var sst = (r[s][0].divide(nums[i]).gcd(nums[i]));
//                    assert r2[i].equals(sst) : r2[i] + " " + r[s][0].divide(nums[i]).gcd(nums[i]);
//                    Logger.getGlobal().warning(sst.toString());
//                }
//            } else {
//                assert Misc.is2Pow(ss) && Misc.is2Pow(nums.length) : ss + " " + nums.length;
//                final BigInteger allP = r[s][0];
//                final int load = nums.length / ss;
//                ExecutorService pool = Executors.newFixedThreadPool(ss);
//                AtomicInteger counter = new AtomicInteger();
//                for (int i = 0; i < ss; i++) {
//                    final int begin = i * load, end = begin + load;
//                    pool.submit(() -> {
//                        for (int j = begin; j < end; j++) {
//                            var sst = allP.divide(nums[j]).gcd(nums[j]);
//                            assert sst.equals(r2[j]);
//                            assert sst.equals(nums[j]);
//                            Logger.getGlobal().info(sst.toString());
//                        }
//                        Logger.getGlobal().info(String.format("thread %d end\n", Thread.currentThread().getId()));
//                        counter.getAndIncrement();
//                    });
//                }
//                pool.shutdown();
//                try {
//                    pool.awaitTermination(10000, TimeUnit.DAYS);
//                } catch (InterruptedException ignored) {
//                }
//                Logger.getGlobal().info(counter.toString());
//            }
//            long end2 = System.nanoTime();
//            Logger.getGlobal().info(String.format("%d, %d, %d, %f", (end1 - start1), (end2 - end1), (end2 - end1) - (end1 - start1), ((double) (end2 - end1)) / (end1 - start1)));
            break;
        }
    }

    /**
     * just for test
     */
    private static int[][] trivialGCD(BigInteger[] nums) {
        final int maxThreadCnt = Runtime.getRuntime().availableProcessors();
        assert Misc.is2Pow(nums.length) : nums.length;
        assert Misc.is2Pow(maxThreadCnt) : maxThreadCnt;
        long t = nums.length * (long) nums.length;
        Logger.getGlobal().info("taskCnt: " + t);
        final int threadCnt = t < maxThreadCnt ? (int) t : maxThreadCnt;
        final long load = t / threadCnt;
        Logger.getGlobal().info(String.format("%d %d", threadCnt, load));
        ExecutorService pool = Executors.newFixedThreadPool(threadCnt);
        FileWriter ans = null;
        try {
            ans = new FileWriter("./ans.txt");
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(0);
        }
        int ass[][] = new int[10][10];
        for (int i = 0; i < threadCnt; i++) {
            final long begin = i * load, end = i * load + load;
            pool.submit(() -> {
                for (long j = begin; j < end; j++) {
                    int x = (int) (j / nums.length), y = (int) (j % nums.length);
                    ass[0][0] = nums[x].gcd(nums[y]).bitLength();
                }
            });
        }
        pool.shutdown();
        try {
            pool.awaitTermination(10000, TimeUnit.DAYS);
        } catch (InterruptedException e) {
            e.printStackTrace();
            Logger.getGlobal().warning("threadPool await to end failed");
        }
        return ass;
    }
}
