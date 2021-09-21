class A { }

class B inherits A { }

class C inherits A { }

class D inherits C { }

class Main inherits IO {
    main () : Object {
        testing_case()
    };

    testing_case() : IO {
        let a: A <- new D in
            case a of
                x: B => out_string("Is type B.\n");
                x: C => out_string("Is type C.\n");
                x: D => out_string("Is type D.\n");
            esac
    };
}