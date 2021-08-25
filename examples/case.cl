class A inherits D { };

class B inherits D { };

class C inherits B { };

class D {
    p() : String { ", OK?\n" };
};

class Main inherits IO {
    main () : Object {
        let x : D <- new C in class_type(x)
    };

    class_type(var : D) : SELF_TYPE {
        case var of
             a : A => out_string("Class type is now A".concat(a.p()));
             b : B => out_string("Class type is now B".concat(b.p()));
             c : C => out_string("Class type is now C".concat(c.p()));
             d : D => out_string("Class type is now D".concat(d.p())); 
             o : Object => out_string("Oooops");
          esac
    };
};
