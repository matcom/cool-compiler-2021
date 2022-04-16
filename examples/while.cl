class Main inherits IO {
    main() : Object
    {
        let a : Int <- in_int(), i : Int <- 0 in {
            while i < a loop {
                i <- i + 1;
                out_int(i);
                out_string(" ");
            } pool;
	    out_string("\n");
        }
    };
};
