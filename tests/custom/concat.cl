class Main inherits IO {
    main(): IO {
        let a: String <- "x".concat("o") in if a = "xo" then out_string("true") else out_string("false") fi
    };
};
