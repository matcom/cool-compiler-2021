 class Main inherits IO {
  a : A = new A;
    main(): Object
    {  {
      b <- new B;
       a <- (
       case b of
         n : C => n.f();
         n : B => n.f();
       esac);
       out_int(a);
}

  };
};

class A { f():Int { 3 };

class B inherits A { f():Int {4 };

