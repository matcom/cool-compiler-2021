class Main {
  a : A <- new B;
   main(): Int {
     {
       a <- new B;
       a.a();
     }
   };
};

class A {
  aa : Int <- 101;
  a() : Int {
    aa
  };
};

class B inherits A {
  bb : Int <- 102;
  a() : Int {
    100
  };
  b() : Int {
    bb
  };
};