class A inherits B {

};

class B {

};

class Main inherits IO {
    main() : Object {
        let a : B <- new A in out_string(a.type_name().concat("\n"))
    };
};
