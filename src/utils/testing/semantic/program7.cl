class Main {
    main(): Object {
        (new Alpha).print()
    };
};

class Test inherits Object{
    test1: Object;
    test2: Int <- 3;
};

class Test2 {
    test1: Test <- new Test;

    testing1(): Test {
        if 4 < 5 + 6 + 7  then
            while true loop
            { 5; } 
            pool
        else 
            let a: Object in text1 <- (new Test) 
        fi
    };

    testing2(x: Int, y: Int): Test2 {
        self
    };

    testing3(): Test2 {
        testing2(5 + 8, true + false)
    };

    testing4(): Object {
        test1@Object.copy()
    };
};

class Alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};