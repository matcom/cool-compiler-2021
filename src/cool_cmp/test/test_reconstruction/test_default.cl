class B
{
}


class Main inherits IO
{
    a:Int;
    s:String;
    b:Bool;
    o:Object;
    o2:B;
    main(): Bool
    {
        {
            if
                (a = 0)
            then
                if
                    (s = "")
                then
                    if
                        not b
                    then
                        if
                            (o = o2)
                        then
                            true
                        else
                            false
                        fi
                    else
                        false
                    fi
                else
                    false
                fi
            else
                false
            fi;
        }
    };
}


