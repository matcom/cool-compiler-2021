class Main
{
    main(): Object
    {
        self
        .f(
            1,
            1
        )
    };
    f(a:Int, b:Int): Object
    {
        if
            (a = 1)
        then
            b
        else
            self
            .g(
                (a + 1),
                (b / 2)
            )
        fi
    };
    g(a:Int, b:Int): Object
    {
        if
            (b = 1)
        then
            a
        else
            self
            .f(
                (a / 2),
                (b + 1)
            )
        fi
    };
}


