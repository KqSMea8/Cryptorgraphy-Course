import HZeXLibs.util.Misc;

import java.math.BigInteger;
import java.util.Arrays;
import java.util.concurrent.ExecutorCompletionService;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.logging.Logger;

public class ParallelBatchGCD {
    private final int MaxThreadCnt;
    private final int DefaultMinEachThreadLoad;

    public ParallelBatchGCD() {
        this.MaxThreadCnt = Misc.floorTo2Pow(Runtime.getRuntime().availableProcessors());
        this.DefaultMinEachThreadLoad = 256;
    }

    /**
     * the <code>maxThreadCnt</code> will be change to the closet number of 2 pow
     */
    public ParallelBatchGCD(int maxThreadCnt) {
        this.MaxThreadCnt = Misc.closest2Pow(maxThreadCnt);
        this.DefaultMinEachThreadLoad = 256;
    }

    public BigInteger[] worker(BigInteger[] modulus) {
        return remainderTree(productTree(modulus));
    }

    /**
     * @param nums: the nums.length must be 1<<n
     * @return the productTree list
     * <p>use package private just for test </p>
     */
    BigInteger[][] productTree(final BigInteger[] nums) {
        assert Misc.is2Pow(nums.length);
        int tmp_1 = Misc.bitLen(nums.length), tmp_2 = nums.length;
        final BigInteger[][] result = new BigInteger[tmp_1][];
        for (int i = 0; i < tmp_1; i++) {
            result[i] = new BigInteger[tmp_2];
            tmp_2 /= 2;
        }
        assert result[tmp_1 - 1].length == 1;
        System.arraycopy(nums, 0, result[0], 0, nums.length);
        ExecutorService pool = Executors.newFixedThreadPool(computeNeedThread(nums.length, 2)[0]);
        ExecutorCompletionService<Object> cPool = new ExecutorCompletionService<>(pool);
        for (int i = 0; i < tmp_1 - 1; i++) {
            int taskCnt = nums.length / (1 << i);
            var ss = computeNeedThread(taskCnt, 2);
            Logger.getGlobal().info(Arrays.toString(ss));
            int threadCnt = ss[0], eachLoad = ss[1];
            assert Misc.is2Pow(eachLoad) && taskCnt > 0 : taskCnt;
            for (int j = 0; j < threadCnt; j++) {
                final int sb = j * eachLoad, se = j * eachLoad + eachLoad, sl = i, dl = i + 1;
                cPool.submit(() -> {
                    for (int k = sb; k < se; k += 2) {
//                        Logger.getGlobal().warning(String.format("i: %d, thread: %d\n", k - sb, Thread.currentThread().getId()));
                        result[dl][k / 2] = result[sl][k].multiply(result[sl][k + 1]);
                    }
                    return null;
                });
            }
            // when the InterruptedException is thrown,
            // the working thread is not interrupted, so just try to take again
            for (int j = 0; j < threadCnt; j++) {
                try {
                    cPool.take();
                } catch (InterruptedException ignored) {
                    j--;
                }
            }
        }
        pool.shutdownNow();
        return result;
    }

    /**
     * @param tree the tree[0] is the original number array
     *             <p> use package private just for test </p>
     */
    BigInteger[] remainderTree(BigInteger[][] tree) {
        if (tree.length < 2) {
            return new BigInteger[]{BigInteger.ZERO};
        }
        assert Misc.is2Pow(tree[0].length);
        assert Misc.is2Pow(this.MaxThreadCnt);
        int t1 = tree[1].length, t2 = t1 < this.MaxThreadCnt ? t1 : this.MaxThreadCnt;
        assert Misc.is2Pow(t2);
        ExecutorService pool = Executors.newFixedThreadPool(t2);
        ExecutorCompletionService<Object> cPool = new ExecutorCompletionService<>(pool);
        BigInteger[][] result = new BigInteger[2][];
        result[0] = new BigInteger[tree[0].length];
        result[1] = new BigInteger[tree[0].length];
        int resIndex = 0;
        result[0][0] = tree[tree.length - 1][0];
        int tmp = Misc.bitLen(t2);
        Logger.getGlobal().info(String.format("nm len: %d", tree[tree.length - 1][0].bitLength()));
        for (int i = 1; i < tmp; i++) {
            int tc = 1 << i;
            Logger.getGlobal().info(String.format("stage 1, threadCnt: %d", tc));
            for (int j = 0; j < tc; j++) {
                // sl is source line, si is source index
                final int si1 = j / 2, si2 = j, sl1 = resIndex, sl2 = tree.length - 1 - i, dl = (resIndex + 1) % 2;
                cPool.submit(() -> {
                    result[dl][si2] = result[sl1][si1].mod(tree[sl2][si2].pow(2));
//                    Logger.getGlobal().info(String.format("thread %d end", Thread.currentThread().getId()) + " " + result[dl][si2]);
                    return null;
                });
            }
            for (int j = 0; j < tc; j++) {
                try {
                    cPool.take();
                } catch (InterruptedException ignored) {
                    j--;
                }
            }
            resIndex = (resIndex + 1) % 2;
            StringBuilder info = new StringBuilder("time: " + i + ", allLen: ");
            for (int j = 0; j < tc; j++) {
                info.append(result[resIndex][j].bitLength()).append(", ");
            }
            Logger.getGlobal().info(info.toString());
        }
        for (int i = tmp; i < tree.length; i++) {
            final int load = tree[tree.length - 1 - i].length / this.MaxThreadCnt;
            Logger.getGlobal().info("stage 2, load: " + String.valueOf(load) + " threadCnt: " + String.valueOf(this.MaxThreadCnt));
            assert tree[tree.length - 1 - i].length % this.MaxThreadCnt == 0;
            assert (load & 1) == 0 : load;
            for (int j = 0; j < this.MaxThreadCnt; j++) {
                final int sl1 = resIndex, sl2 = tree.length - 1 - i, sib1 = j * load, dl = (resIndex + 1) % 2;
                cPool.submit(() -> {
                    for (int k = 0; k < load; k++) {
                        result[dl][sib1 + k] = result[sl1][(sib1 + k) / 2].mod(tree[sl2][(sib1 + k)].pow(2));
//                        Logger.getGlobal().warning(result[sl1][(sib1 + k) / 2] + " " + result[dl][sib1 + k]);
                    }
                    return null;
                });
            }
            for (int j = 0; j < this.MaxThreadCnt; j++) {
                try {
                    cPool.take();
                } catch (InterruptedException e) {
                    j--;
                }
            }
            resIndex = (resIndex + 1) % 2;
        }
        var s = computeNeedThread(tree[0].length, 1);
        final int sl = resIndex, dl = (resIndex + 1) % 2, threadCnt = s[0], load = s[1];
        Logger.getGlobal().info(String.format("stage 3, threadCnt: %d, load: %d", threadCnt, load));
        for (int i = 0; i < threadCnt; i++) {
            final int b = i * load, e = i * load + load;
            cPool.submit(() -> {
                for (int j = b; j < e; j++) {
                    var k = result[sl][j].divideAndRemainder(tree[0][j]);
                    assert k[1].equals(BigInteger.ZERO);
                    result[dl][j] = k[0].gcd(tree[0][j]);
                }
                return null;
            });
        }
        for (int i = 0; i < threadCnt; i++) {
            try {
                cPool.take();
                Logger.getGlobal().info(String.format("stage 3, take: %d", i));
            } catch (InterruptedException e) {
                i--;
            }
        }
        pool.shutdownNow();
        return result[dl];
    }

    /**
     * @param minEachThreadLoad if <code>minEachThreadLoad</code> <=0, then use default load
     * @return (a, b), a is the threadCnt, b is the load of each thread
     */
    private int[] computeNeedThread(int taskCnt, int minEachThreadLoad) {
        if (minEachThreadLoad <= 0) {
            minEachThreadLoad = DefaultMinEachThreadLoad;
        }
        if (taskCnt <= 0) {
            return new int[]{0, 0};
        }
        int t = taskCnt / minEachThreadLoad + ((taskCnt % minEachThreadLoad == 0) ? 0 : 1);
        t = t < this.MaxThreadCnt ? t : this.MaxThreadCnt;
        int r = taskCnt / t + (taskCnt % t == 0 ? 0 : 1);
        return new int[]{t, r};
    }
}
