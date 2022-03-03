class Main inherits IO {
    msg : String <- "Hello world!";
    a : Int <- 2;
    b : Int <- 5;

    main() : IO {
        self.out_string(msg.substr(a, b))
    };
};