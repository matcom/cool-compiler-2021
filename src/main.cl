(*
class Main {
    number: Int <- 0;

    main() : Object {
        let x: Int <- number + 2, io: IO <- new IO, p: Point <- (new Point).init(1, 2) in {
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
    point: Point;

    init (x0: Int, y0: Int): Point{
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

class Point3D inherits Point {
    z: Int <- 0;

    init (x0: Int, y0: Int): Point{
        {
            z <- 0;
            self@Point.init(x0, y0);
        }
    };

    get_z(): Int {
        z
    };
};
*)

class Main inherits IO {
    main() : Object {
        -- out_string("Hello, World!\n")
        out_int((2 + 2) * 2)
    };

--     plus(a: Int, b: Int) : Int {
--         a + b
--     };

--     minus(a: Int, b: Int) : Int {
--         a - b
--     };

--     mult(a: Int, b: Int) : Int {
--         a * b
--     };

--     div(a: Int, b: Int) : Int {
--         a / b
--     };

--     equals(a: Bool, b: Bool) : Bool {
--         a = b
--     };

--     less(a: Int, b: Int) : Bool {
--         a < b
--     };
    
--     less_equals(a: Int, b: Int) : Bool {
--         a <= b
--     };
};
