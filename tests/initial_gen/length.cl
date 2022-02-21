class Main inherits IO {
    msg: String <- "Hello";
    main() : AUTO_TYPE {
        out_int(msg.length())
    };
};
