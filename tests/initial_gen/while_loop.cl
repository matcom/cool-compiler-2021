class Main inherits IO {
    a: Int <- 10;
    main() : AUTO_TYPE {
        while not a <= 0 loop {
            a <- a - 1;
            out_int(a);
        } pool
    };
};