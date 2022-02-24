class Main {
   -- main () : AUTO_TYPE { method(1,2,3,4,5,6) };
   main(): Int {0};

    method(a : AUTO_TYPE, b: AUTO_TYPE, c: AUTO_TYPE, d : AUTO_TYPE, e: AUTO_TYPE, f: AUTO_TYPE): AUTO_TYPE{{
        a <- e;
        b <- a;
        c <- b;
        d <- c;
        e <- f;
        f + 12; 
    }}; 
};