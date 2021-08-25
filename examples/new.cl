class Main inherits IO {
    main() : Object
    {
        let a : A <- new A in if a.f() then out_string("TRUE!!!\n") else out_string("FALSE!!!\n") fi
    };
};

class A {
    a : Int <- 5;
    b : B;

    f() : Bool { isvoid b };
};

class B {
    
};
