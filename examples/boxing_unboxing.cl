class Main inherits IO {
    main() : Object {
        {
        	out_string(5.type_name());
		out_string("\n");
        	out_string(f(5));
		out_string("\n");
        	let x : Object <- 5 in out_string(x.type_name());
		out_string("\n");
        	let y : Int <- 5.copy() + 5 in out_int(y);
		out_string("\n");
    	}
    };

    f(x :  Object) : String {
        x.type_name()
    };
};
