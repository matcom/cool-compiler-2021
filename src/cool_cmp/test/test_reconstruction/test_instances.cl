class Main
{
    a:Int;
    set(v:Int): Int
    {
        a <- 
            v
    };
    get(): Int
    {
        a
    };
    main(): Int
    {
        {
            a <- 
                10;
            b:Main <- 
                self
                .copy(
                );
            a <- 
                20;
            (                b
                .get(
                )
 +                 self
                .get(
                )
);
        }
    };
}


