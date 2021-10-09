class A inherits IO
{
    p(): Int
    {
        0
    };
}


class Main inherits A
{
    msg:String <- "Hello World";
    p(): Int
    {
        1
    };
    main(): Int
    {
        let
            x0:Int <- 
                0,
            x1:Int <- 
                1,
            x2:Int <- 
                let
                    x1:Int <- 
                        2,
                    x2:Int <- 
                        (x1 + 1)
                in
                    ((x0 + x1) + x2)
        in
            (x1 + x2)
    };
}


