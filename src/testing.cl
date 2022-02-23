class A{
};

class B inherits A {
};

class Main inherits IO {
    main() : AUTO_TYPE {
        out_int(case new B of 
            a: A => 1;
            b: B => 2;
        esac)
    };
};
