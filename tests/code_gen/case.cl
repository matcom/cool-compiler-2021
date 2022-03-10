


class Main inherits IO{
    a : A <- new B;
    b : B <- new B;
    c : String <- "First sentence.";
    d : String <- "Second sentence.";
    g : String <- "Second sentence.";
    main (): Object {
        {
            out_string(
                (case a of
                    h:A => new A;
                    f:B => new B;
                esac).type_name()
            ); 
        }
    };
};

class A {

};

class B inherits A{

};

