class A
{
    m1(): Int
    {
        10
    };
}


class B
{
    m1(): Int
    {
        20
    };
}


class Main inherits IO
{
    main(): Int
    {
        10
    };
    m(a:AUTO_TYPE): Int
    {
        a
        .m1(
        )
    };
}


