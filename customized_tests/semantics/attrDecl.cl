class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };

class Main inherits IO {
	test1: X <- new Main;

	main(): IO { out_string("Hello World!")};
};