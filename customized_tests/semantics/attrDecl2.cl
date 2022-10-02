class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };

class Main inherits W {
	test1: X <- new Main;

	main(): G { out_string("Hello World!")};
};