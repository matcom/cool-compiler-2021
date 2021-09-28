class Main inherits IO {

	msg:String <- "Hello World";

    main(): IO {
		--new IO
        out_string(msg)
    };
};
