- 需要使用connect函数才能使得connect有效
   ```java
    var connection = (HttpsURLConnection) new URL(url).openConnection();
    connection.setConnectTimeout(2000);
    connection.setRequestMethod("HEAD");
    connection.connect();
   ```
- threadPool 会抑制所有异常，除非自己有处理。所以前面我没有connect后抛异常但是我不知道还以为是诸如c lib的bug
- properties文件的key value都不需要带分号的双引号，即使使用get方法读到的也不能转为Integer，要parseInt（幸好不能转，要是强转成功那就gg了）
- condition 使用时需要结合lock，不然会抛异常
- condition的notify与signal，至少我使用notify我的await老是醒不了
- `FileWriter`的write方法并不能保证所有要写的东西要么都写进去要么都不写进去，所以要自己catch异常然后进行处理
- 如果某个线程不拥有一个lock，然后调用unlock会IllegalMonitorStateException，即使有其他线程lock了
- 跑着跑着总是会整个停下来，jstack看似乎除了await pool停止的那个控制线程外其他线程都处在socket上（不知道为什么超时1ms就不会1000ms就会）。猜测是等线程的所有thread用完了pool可以用的所有线程，然后本来能跑的就都gg了。试了试以下代码，确实如此
   ```java
    public static void main(String[] argv) throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(10);
        for (int i = 0; i < 9; i++) {
            pool.submit(() -> {
                while (true) {

                }
            });
        }
        for (int i = 0; i < 10; i++) {
            pool.submit(() -> System.out.println(Thread.currentThread().getId()));
        }
        pool.shutdown();
        pool.awaitTermination(1000, TimeUnit.DAYS);
    }
    // output are all 22, if the first loop is `i<10`, then no output
    // jstack report that all thread is run(10 threads)
   ```
   解决方法还是要靠socket的timeout，不过现在搞不了。然后就试着开大量线程，然后等到只有少量线程的时候就cut掉
- 奇怪现象：这个进程是29264，我不小心dump了29265的 stack，然后输出idea就显示我的dump的结果了。
- 之所以线程一直被hang住，是因为没有设置readTimeOut，设置了之后就没问题了