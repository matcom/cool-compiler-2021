 class Main inherits IO {
  a : Int;
  b : A;
    main(): Object
    {  {
      b <- new B;
       a <- (
       case b of
         n : Bool => 1;
         n : Int => 2;
         n : Object => 5;
         n : String => 3;
        n : A => 7;
       esac);
       out_int(a);
}

  };
};

class A { };

class B inherits A { };

class C inherits B { };
