class Main inherits IO {
    msg : String <- "Hello world";

    main() : IO {
        let y : String <- msg.substr(2, 2) in {
            self.out_int(y.substr(0, 1).length());
        }
    };
};
