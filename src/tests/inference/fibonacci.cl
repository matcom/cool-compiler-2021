class Main {
    main (): Int {
        1
     };

    iterative_fibonacci(n: AUTO_TYPE) : AUTO_TYPE {
        let  i: AUTO_TYPE <- 2, n1: AUTO_TYPE <- 1, n2: AUTO_TYPE <- 1 in {
            while i < n loop
                let temp: AUTO_TYPE <- n2 in {
                    n2 <- n2 + n1;
                    n1 <- temp;
                    i <- i + 1;
                }
            pool;
            n2;
            }
        };
};