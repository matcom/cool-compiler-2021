class Main
{
    main(): Object
    {
        {
            a:Object <- 
                case
                    (20 + 40)
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


