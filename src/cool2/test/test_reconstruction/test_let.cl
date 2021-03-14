class Main
{
    b:Bool;
    main(): Int
    {
        {
            a:Int <- 
                let
                    a:Bool <- 
                        true,
                    a:Int <- 
                        if
                            a
                        then
                            10
                        else
                            20
                        fi
                in
                    a;
            c:Int <- 
                let
                    a:SELF_TYPE <- 
                        self
                        .change(
                        ),
                    b:Int <- 
                        if
                            b
                        then
                            10
                        else
                            20
                        fi
                in
                    b;
            (a + c);
        }
    };
    change(): SELF_TYPE
    {
        {
            b <- 
                not b;
            self;
        }
    };
}


