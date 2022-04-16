class Main inherits IO {
    main() : Object {
        out_int(f(in_int(), in_int()))
    };

    f(x : Int, y : Int) : Int {
        x / y
    };
};
