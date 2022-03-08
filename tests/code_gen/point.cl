class Main inherits IO{
    main (): Object {
	out_int((new Point).init(5, 6))
        
    };
};

class Point{
    x: Int;
    y: Int;

    init(x0: AUTO_TYPE, y0: AUTO_TYPE): AUTO_TYPE {
	x0 + y0 
    };
};
