class Main inherits IO {
    msg : String <- "Hello World";

    main() : IO{
        out_string(msg)
    };
};