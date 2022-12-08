 class Main inherits IO {
	a : A;
	main(): Main {
		{
		a <- new B;
		out_int(a.f());
		}		
	};
};

class A {
	a : Int;
	f() : Int {
	1
	};
};

class B inherits A{
	f() : Int {
		{ a <- 12; a; }
	};
};

