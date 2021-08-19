class A {
	a: Int;
};

class B inherits A {
	b: Int;
};

class C inherits B {
	c: Int;
};

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
	test: Int <- let x: Int <- 1 in x;
};
