class A{
    a:SELF_TYPE;
    get():SELF_TYPE {
        self
    };
    get2():SELF_TYPE {
        new SELF_TYPE
    };
    get3():SELF_TYPE {
        {
            a  <- new SELF_TYPE;
            a;
        }
    };
};

class B inherits A {
    get4(): SELF_TYPE {
        get3()
    };
 };

class Main inherits IO {
    main() : AUTO_TYPE {
        out_int(case new B of 
            obj: Object => 0;
            a: A => 1;
            b: B => 2;
        esac)
    };
};
