class Main inherits IO {
    main() : AUTO_TYPE {
		{
			out_string(1.type_name());
			out_string(false.type_name());
			out_string(true.type_name());
			true.abort();
		}
    };
};
