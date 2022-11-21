class Main {
    main (): AUTO_TYPE {{
        (new Point).init(3, 4);
        new IO.out_string("done\n");
    }};
};

class Point {
    x: Int;
    y: Int;

    init(x0: AUTO_TYPE, y0: AUTO_TYPE): AUTO_TYPE {{
        x <- x0;
        y <- y0;
        x + y;
    }};
};
