class Main
{
    main(): Object
    {
        {
            a:Object <- 
                case
                    while
                        false
                    loop
                        1
                    pool
                of
                    b:Int =>
                        if
                            (b = 60)
                        then
                            50
                        else
                            0
                        fi;
                    c:Object =>
                        c;
                esac;
            a;
        }
    };
}


