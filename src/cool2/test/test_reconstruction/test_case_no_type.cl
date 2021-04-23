class Main
{
    main(): Object
    {
        {
            a:Object <- 
                case
                    (20 + 40)
                of
                    a:Bool =>
                        if
                            a
                        then
                            true
                        else
                            false
                        fi;
                esac;
            a;
        }
    };
}


