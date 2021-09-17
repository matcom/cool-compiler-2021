class A
{
    a:Int;
    a(a:Object): Object
    {
        a
    };
}


class B inherits A
{
    a(self:Int): Object
    {
        a
    };
}


class Main inherits IO
{
    main(): B
    {
        new B
    };
}


