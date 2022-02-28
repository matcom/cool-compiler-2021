class Main inherits IO {
  attM : B <- new B;
   main(): IO {
    case attM of
      attA : A => out_int(1);
      attB : B => out_int(2);
      attO : Object => out_int(0);
    esac
   };
};

class A {
  atta : Int <- 1;
  fa() : Int {
    atta
  };
};

class B inherits A {
  attb : Int <- 2;
  fb() : Int {
    attb
  };
};