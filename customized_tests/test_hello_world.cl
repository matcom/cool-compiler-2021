class Main inherits IO {
    msg : String <- " Hello World ";

    main() : IO{
        self.print(msg)
    };
};