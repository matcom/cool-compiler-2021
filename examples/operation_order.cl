class Main inherits IO {
    main() : Object
    {
        let a : Int <- 1, b : Int <- 2, c : Int <- 3, d : Int <- 4 in 
        {
            out_int(a * b + c * d);       -- 14
            out_string(" ");
            out_int(a / (b - c) * d);     -- -4
	    out_string("\n");
        }
    };
};
