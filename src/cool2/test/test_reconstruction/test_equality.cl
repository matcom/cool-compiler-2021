class A
{
}


class B
{
}


class Main
{
    cClass:A;
    dClass:B;
    main(): Bool
    {
        {
            aClass:A <- 
                new A;
            bClass:A <- 
                new A;
            a:Bool <- 
                (aClass = aClass);
            b:Bool <- 
                not (aClass = bClass);
            c:Bool <- 
                (cClass = dClass);
            ((c = (a = b)) = true);
        }
    };
}


