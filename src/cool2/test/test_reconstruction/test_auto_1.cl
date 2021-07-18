class Main inherits IO
{
    main(): Main
    {
        let
            x:Int <- 
                (3 + 2)
        in
            {
                case
                    x
                of
                    y:Int =>
                        self
                        .out_string(
                            "Ok"
                        );
                esac;
            }
    };
}


