--The type of an initialization expression must conform to the declared type of the identifier.

class A { };
class B inherits A { };
class C inherits B { };

class Main inherits IO {
	test: B <- let a: Bool, a: Int <- 5, a: String, b: C <- new C in b;

	main(): IO { out_string("Hello World!")};

	get_test(): B { test };
};