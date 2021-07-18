class Test
{
    test3:Int <- (test + test2);
    test2:Int <- (2 * test);
    test:Int <- 10;
}


class Main inherits Test
{
    main(): Int
    {
        {
            test3;
        }
    };
}


