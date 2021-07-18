class Test
{
    test:Int <- 10;
    test2:Int <- 20;
}


class Main inherits Test
{
    test3:Int <- (test + test2);
    main(): Int
    {
        {
            test3;
        }
    };
}


