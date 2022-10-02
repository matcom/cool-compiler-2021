
class Main inherits IO{
    a : Int <- 5;
    b : Int <- 4;
    main (): Object {
        {
             
           a < b;
             a <= b; 
            a = b;
            
            out_string(if a < b then "a<b" else "a>=b" fi);
        }
    };
};
