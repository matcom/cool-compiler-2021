class Main {

    main() : Object {
        let io: IO <- new IO, p: Point <- (new Point).init(5, 6) in {
            io.out_string("(");
            io.out_int(p.get_x());
            io.out_string(",");
            io.out_int(p.get_y());
            io.out_string(")");
            io.out_string("\n");
        }
    };
};

class Point {
    x: Int <- 0;
    y: Int <- 0;

    init (x0: Int, y0: Int ): Point{
        {
            x <- x0;
            y <- y0;
            self;
        }
    };

    get_x(): Int {
        x
    };

    get_y(): Int {
        y
    };
};