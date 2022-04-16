class A inherits IO {
    identify() : Object{out_string("I am of type A!!!\n")};
};

class B inherits A {
    identify() : Object{out_string("I am of type B!!!\n")};
};

class Main inherits IO {
    main() : Object {
        {
            let me : A <- new A in me@A.identify();

            let me : A <- new B in me@A.identify();

            let me : B <- new B in {
                me@A.identify();
                me@B.identify();
            };
        }
    };
};
