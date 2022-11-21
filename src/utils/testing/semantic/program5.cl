class Main {
    main(): Object {
        (new Alpha).print()
    };
};
class Alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};