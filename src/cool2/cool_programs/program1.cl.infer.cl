class B
{
}


class Main
{
    main(): Bool
    {
        {
            a:Int <- 
                20;
            b:Int <- 
                30;
            c:B <- 
                new B;
            d:String <- 
                "hello";
            e:String <- 
                "olleh";
            f:Bool <- 
                false;
            g:Bool <- 
                true;
            r1:Int <- 
                (a + b);
            r2:Object <- 
                (a + c);
            r3:Object <- 
                (a + d);
            r4:Object <- 
                (e + d);
            r5:Int <- 
                ~ a;
            r6:Object <- 
                ~ c;
            r7:Object <- 
                ~ d;
            r8:Object <- 
                not a;
            r9:Object <- 
                not c;
            r10:Object <- 
                not d;
            r11:Bool <- 
                (a = b);
            r12:Bool <- 
                (c = b);
            r13:Bool <- 
                (d = b);
            r14:Bool <- 
                (d = e);
            r15:Object <- 
                (f + a);
            r16:Object <- 
                (f + d);
            r17:Object <- 
                ~ f;
            r18:Bool <- 
                not f;
        }
    };
}


