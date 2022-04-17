class Main {
    x : Sally <- (new Sally).copy();
    main() : Sally {
        x
    };
};

class Silly {
    a: Int <- 10;
    copy() : SELF_TYPE {
        self
    };
};

class Sally inherits Silly {
    y : String <- "Hi from Silly";
};
