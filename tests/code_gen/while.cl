class Main inherits IO{
    a : Int <- 0;
    b : Int <- 3;
    main (): Object {
        {   
            while a < b loop {
                out_int(a);
                out_string("iteration \n");
                a <- a + 1;
                } 
            pool;
        }
    };
};