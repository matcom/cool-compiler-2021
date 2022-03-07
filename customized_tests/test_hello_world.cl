(* class Main inherits IO {
    msg : String <- "Hello World";

    main() : IO{
        self@IO.out_string(msg)
    };
};
*)



class Main inherits IO{
    main (): Object {
	self@IO.out_int((new Point)@Point.init(5, 6))
        
    };
};

class Point{
    x: Int;
    y: Int;

    init(x0: AUTO_TYPE, y0: AUTO_TYPE): AUTO_TYPE {
	x0 + y0 
    };
};

