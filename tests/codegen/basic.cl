class Main inherits IO {
   a : A <- new B;
   main(): Int {
	out_string("Hello, World.\n")
   };
};

class A : Int{
   aa : Int <- 101;
   a(): Int {
   	aa
   };
};
class B : Int{
   bb : Int <- 102;
   a(): Int {
   	bb
   };
};
