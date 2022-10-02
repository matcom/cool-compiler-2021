
class Main inherits IO{
    a : Int;
    b : Int;
    c : String <- "First sentence.";
    d : String <- "Second sentence.";
    main (): Object {
        {
            out_string(c.concat(d)); 
            out_string(c.substr(0, c.length()));
        }
    };
};
