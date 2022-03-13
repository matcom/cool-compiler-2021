class Main{
    main():Int{ 0 };
};

class A inherits IO{
    g1(a:Int):Int{3};
 };

class B inherits A {
    g2(a:Int):Int{3};
    g3(a:Int):Int{3};
 };

class C inherits B { 
    test: Int <- 3;
    g4(a:Int):Int{3};
};

