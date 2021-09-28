class Main inherits IO
{
    msg:String <- "Hello World";
    main(): IO
    {
        self
        .out_string(
            msg
        )
    };
}


