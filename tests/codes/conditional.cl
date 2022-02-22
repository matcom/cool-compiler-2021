--The predicate must have static type Bool.

class A { };
class B inherits A { };
class C inherits B { };

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
	a: A <- if let x: Bool <- true in x then new B else new C fi;
};