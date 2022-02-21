class A
{
    get(): SELF_TYPE
    {
        self
    };
    get2(): SELF_TYPE
    {
        new SELF_TYPE
    };
};


class B inherits A
{
   
};


class Main inherits IO
{
    main(): AUTO_TYPE
    {
        {
            let b:B <- 
                    new B in
            out_string(b.get().type_name().concat(b.get2().type_name().concat(b.type_name())));
        }
    };
};


