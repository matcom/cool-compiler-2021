class Main inherits IO {
    main(): IO {
        (let a: String <- "hello, ", b: String <- "world\n" in
         out_string(a.concat(b).substr(7, 7)))
    };
};
