class Main inherits IO {
    i: Int <- 0;

    main(): Object {
        while i < 10 loop {
            i <- i + 1;
            out_int(i);
        } pool
    };
};
