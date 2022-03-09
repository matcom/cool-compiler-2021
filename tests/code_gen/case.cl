


class Main inherits IO{
    a : A <- new A;
    b : B <- new B;
    c : String <- "First sentence.";
    d : String <- "Second sentence.";
    g : String <- "Second sentence.";
    main (): Object {
        {
            out_string(
                (case c of
                    h:String => h <- "Modified.";
                    f:A => d;
                esac).concat(d)
            ); 
        }
    };
};

class A {

};

class B inherits A{

};

