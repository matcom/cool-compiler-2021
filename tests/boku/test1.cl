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
	main(): Int { a.f1() };
	test: Int <- let x: Int <- 1 in x;
};
