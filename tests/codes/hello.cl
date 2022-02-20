class Main inherits IO {
    msg : String <- "Hello World!\n";

    main() : IO {
        self.out_string(msg)
    };
};

(*
    .TYPES
    type Main {
        attribute Main_msg ;
        method Main_main: f1 ;
    }

    .DATA
    s1 = "Hello World!\n";

    .CODE
    function entry {
        LOCAL lmsg ;
        LOCAL instance ;
        LOCAL result ;

        lmsg = LOAD s1 ;
        instance = ALLOCATE Main ;
        SETATTR instance Main_msg lmsg ;

        ARG instance ;
        result = VCALL Main Main_main ;

        RETURN 0 ;
    }

    function f1 {
        PARAM self ;

        LOCAL lmsg ;

        lmsg = GETATTR self Main_msg ;
        PRINT lmsg ;

        RETURN self ;
    }
*)