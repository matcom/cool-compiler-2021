class B {}

class Main {
    main() : AUTO_TYPE
    {
        {
            a:Int <- 20;
            b:Int <- 30;
            c:B <- new B;
            d:String <- "hello";
            e:String <- "olleh";
            f:Bool <- false;
            g:Bool <- true;

            r1:AUTO_TYPE <- a + b;
            r2:AUTO_TYPE <- a + c;
            r3:AUTO_TYPE <- a + d;
            r4:AUTO_TYPE <- e + d;
            r5:AUTO_TYPE <- ~a;
            r6:AUTO_TYPE <- ~c;
            r7:AUTO_TYPE <- ~d;
            r8:AUTO_TYPE <- not a;
            r9:AUTO_TYPE <- not c;
            r10:AUTO_TYPE <- not d;
            r11:AUTO_TYPE <- a = b;
            r12:AUTO_TYPE <- c = b;
            r13:AUTO_TYPE <- d = b;
            r14:AUTO_TYPE <- d = e;
            r15:AUTO_TYPE <- f + a;
            r16:AUTO_TYPE <- f + d;
            r17:AUTO_TYPE <- ~f;
            r18:AUTO_TYPE <- not f;
        }
    };
}