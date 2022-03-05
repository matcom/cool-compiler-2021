class Foo {
    a: Int <- 1;
};

class Bar inherits Foo {
    b: Int <- 2;
};

class Main inherits Bar {
    main(): IO {
        let io: IO <- new IO, test: Object <- self in
        case test of
		    n : Bar => io.out_string("Bar");
            n : Foo => io.out_string("Foo");
            n : Object => io.out_string("Object");
			n : Main => io.out_string("Main");
		esac
    };
};
