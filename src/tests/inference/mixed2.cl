class Main {
    main() : Int {0};

    s : AUTO_TYPE <- method1(s); -- esto debe dar error semantico porque 's'
                                 -- todavia no esta definida cuando se pasa como 
                                 -- parametro ???

    method0( a: A) : AUTO_TYPE {
        {
            a;
        }
    };

    d : B;
    method1(a: AUTO_TYPE) : AUTO_TYPE {
        {
            method0(a);
            d <- a;
            a;
        }
    };
};

class A {

};

class B inherits A {

};

class C inherits B {

};