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
        out_string(let a:A <- new A, b:B <- new B in
            b.get().type_name().concat(
            b.get2().type_name()).concat(
            b.get3().type_name()).concat(
            b.get4().type_name()).concat(
            type_name()))
    };
};
