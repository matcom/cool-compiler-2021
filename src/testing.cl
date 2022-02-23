class A{
};

class B inherits A {
};

class C inherits A{
};

class Main inherits IO {
   a:A;
    main() : AUTO_TYPE {
        out_int(case a of 
            a: A => 7;
            b: B => 13;
            c: C => 123;
        esac)
    };
};
