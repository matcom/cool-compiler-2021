class Main inherits IO {
   b : B <- new B;
   main(x: Int): IO {
	out_int(b.a())
   };
};

class A {
   aa : Int;
   a(): Int {
      aa
   };
};

class B inherits A{
   bb : Int;
   b(): Int {
      bb
   };
};