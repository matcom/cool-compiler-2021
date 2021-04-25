--The static types of the two sub-expressions must be Int.

class Main {
	a : B <- new B;
	b : B;
	main(): B {
		{
			b <- a.method(); 
			b;
		}
	};
};

class A {
	method(): SELF_TYPE {
		new A
	};
};

class B inherits A {
	
};