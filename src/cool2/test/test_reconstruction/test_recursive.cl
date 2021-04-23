class Main
{
    main(): Int
    {
        self
        .fibo(
            7
        )
    };
    fibo(n:Int): Int
    {
        if
            (n > 1)
        then
            (                self
                .fibo(
                    (n - 1)
                )
 +                 self
                .fibo(
                    (n - 2)
                )
)
        else
            1
        fi
    };
}


