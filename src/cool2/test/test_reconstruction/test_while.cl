class Main inherits IO
{
    main(): Int
    {
        {
            counter:Int <- 
                0;
            a:Object <- 
                while
                    (counter < 10)
                loop
                    counter <- 
                        (counter + 1)
                pool;
            counter;
        }
    };
}


