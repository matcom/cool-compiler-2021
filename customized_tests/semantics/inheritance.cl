class A inherits B{ };
class B inherits C { };
class C inherits A { };
class D inherits B { };

class Main inherits A {
	test1: B <- new Main;

	main(): C { out_string("Hello World!")};
};