
class Main inherits IO{
    c : String <- "First sentence.\n";
    d : Int <- 1; 
    main (): Object {
        {
            out_string(c.copy()); 
            out_string(c.type_name());
            
            
        }
    };
};
