class A inherits IO {
    p(): Int {
        0
    };
};

class Main inherits A {

	msg:String <- "Hello World";

    p(): Int {
        1
    };

    main(): AUTO_TYPE {
		--new IO
        --out_string(msg)
        --if not 5 + 10 = 15 then 0 else 1 fi
        --if not 5 + 10 < 15 then 0 else 1 fi
        --while false loop
        --{
        --    3+2;
        --    3-2;
        --}
        --pool
        --self@A.p()
        let x0: Int <- 0,
            x1: Int <- 1, 
            x2: Int <- 
                let x1: Int <- 2, 
                    x2: Int <- x1 + 1 
                in x0 + x1 + x2 
            in x1 + x2 
    };
};
