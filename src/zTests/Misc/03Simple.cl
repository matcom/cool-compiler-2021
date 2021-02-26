
class Main{
    a: A;		
    main(): A {
        1
    };
};

class A {
    oper(a : Int, b : Int): Int{
        a + b
    };
};
class B inherits A {
	oper(a : Int, b : Int, c : Int) : Int{
		a * b * c
	};
};
class C inherits A {
	oper(a : Int, b : String) : Bool{
		a + b
	};
};