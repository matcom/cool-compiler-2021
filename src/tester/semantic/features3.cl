-- Missing type

class Main inherits IO {
	main(): IO { not a+b};

	main: IO <- out_string("bye!");
};

class A {
	x: Int <- 3;

	x(): Int { 3 };

	c: Cadena;
};