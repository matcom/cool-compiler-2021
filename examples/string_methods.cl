class Main inherits IO {
    main() : Object {
        let a : String <- "Jotica", b: String <- "Ariel" in {
        	out_int(a.length());
        	out_string("\n");
        	out_int(b.length());
        	out_string("\n");
        	out_string(a.concat(" ").concat(b));
        	out_string("\n");
        	out_string(a.substr(1,2));
        	out_string("\n");
        }
    };
};
