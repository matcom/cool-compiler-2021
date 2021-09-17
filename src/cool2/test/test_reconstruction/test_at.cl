class A
{
    name(): String
    {
        "class A "
        .concat(
            self
            .name2(
            )
        )
    };
    name2(): String
    {
        "class A"
    };
}


class B inherits A
{
    name(): String
    {
        "class B"
    };
    name2(): String
    {
        "class B"
    };
}


class Main inherits IO
{
    main(): String
    {
        {
            b:B <- 
                new B;
            b
            @A.name(
            );
        }
    };
}


