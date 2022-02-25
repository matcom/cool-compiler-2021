class Main inherits IO {
    arg: String <- "Hello World!";
    main() : IO {
        {
            out_string(arg);
        }
    };
};