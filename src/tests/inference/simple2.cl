class Main {
    main () : Int {0};

    method(a : AUTO_TYPE, b: AUTO_TYPE, c: AUTO_TYPE, d : AUTO_TYPE, e: AUTO_TYPE, f: AUTO_TYPE): AUTO_TYPE{{
        a <- e;
        b <- a;
        c <- b;
        d <- c;
        e <- f;
        f <- 12;
        f; 
    }}; 
};