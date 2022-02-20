class Main inherits IO {

    a:Int <- 0;

    get_a() : Int {
        a
    };

    add_a() : AUTO_TYPE {
        a <- a+1
    };

    main() : AUTO_TYPE {
        {
            a <- 1;
            let b:Main <- copy() in {
                out_int(b.get_a());
                b.add_a();
                out_int(b.get_a());
                out_int(a);
            };
        }
    };
};
