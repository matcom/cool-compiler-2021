class A {
	a: Int;
	f1(): Int { a <- 3 };
};

class B inherits A {
	b: Int;
};

class C inherits B {
	c: Int;
};

class Main inherits IO {
	a: A <- new A;
	main(): Int { { if true then let x: A <- new A in x.f1() else 1 fi; 0; } };
	const(): Int { while 1 loop 0 pool };
	test: Int <- let y: Int <- 1 in y;
};
