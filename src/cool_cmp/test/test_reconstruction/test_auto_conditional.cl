class Base
{
    base(): Base
    {
        self
    };
}


class OtraBase
{
    otraBase(): OtraBase
    {
        self
    };
}


class ConcBase1 inherits Base
{
}


class ConcBase2 inherits OtraBase
{
}


class Main
{
    a:AUTO_TYPE <- new Void;
    main(): Int
    {
        {
            a:OtraBase <- 
                if
                    true
                then
                    new OtraBase
                else
                    new ConcBase2
                fi;
            b:ConcBase2 <- 
                if
                    true
                then
                    new ConcBase2
                else
                    new ConcBase2
                fi;
            c:Object <- 
                if
                    true
                then
                    new ConcBase1
                else
                    new ConcBase2
                fi;
            d:AUTO_TYPE <- 
                if
                    true
                then
                    self
                    .ret1(
                    )
                else
                    self
                    .ret2(
                    )
                fi;
            e:AUTO_TYPE <- 
                if
                    true
                then
                    self
                    .ret1(
                        new ConcBase1
                    )
                else
                    self
                    .ret2(
                        new ConcBase2
                    )
                fi;
            1;
        }
    };
    ret1(): Object
    {
        c:Object <- 
            if
                true
            then
                new ConcBase1
            else
                new ConcBase2
            fi
    };
    ret2(): OtraBase
    {
        c:OtraBase <- 
            if
                true
            then
                new OtraBase
            else
                new ConcBase2
            fi
    };
    ret1(param:Base): Object
    {
        {
            c:Base <- 
                param
                .base(
                );
            a:Object <- 
                case
                    param
                of
                    b:Base =>
                        if
                            true
                        then
                            b
                        else
                            param
                        fi;
                    b:OtraBase =>
                        if
                            false
                        then
                            b
                        else
                            param
                        fi;
                esac;
        }
    };
    ret2(param:OtraBase): Base
    {
        {
            c:OtraBase <- 
                param
                .otraBase(
                );
            a:Base <- 
                case
                    param
                of
                    b:Base =>
                        if
                            true
                        then
                            b
                        else
                            b
                        fi;
                    b:ConcBase1 =>
                        if
                            true
                        then
                            b
                        else
                            b
                        fi;
                esac;
        }
    };
}


