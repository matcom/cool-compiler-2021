class Main inherits IO {
    ack(m: Int, n: Int) : Int {
        if m = 0 then 
            n + 1 
        else if n = 0 then 
                ack(m-1, 1) 
            else 
                ack(m-1, ack(m, n-1)) 
            fi 
        fi
    };
    
    main() : IO {
        out_int(ack(2,3))
    };
};