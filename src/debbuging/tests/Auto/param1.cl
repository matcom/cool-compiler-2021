class Main {
    main() : Int {0};

    s : AUTO_TYPE <- method1(s); --Esto deberia dar error no se puede pasar s xq no debe existir
    f : AUTO_TYPE;
    method0( a: A) : AUTO_TYPE {
        {
            a;
        }
    };

    d : B; 
    method1(a: AUTO_TYPE) : AUTO_TYPE {
        {
            method0(a);
            d <- a; -- si se comenta esta linea 'a' deberia ser de tipo "A, B o C" si no, de tipo "B o C"
            1;
        }
    };
};

class A {

};

class B inherits A {

};

class C inherits B {

};
