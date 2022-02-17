class Main {
    main (): AUTO_TYPE {
        (new IO).out_string("Done\n")
    };

    func (x: AUTO_TYPE, y: AUTO_TYPE, z: AUTO_TYPE): Int {
        {
            x <- y;
            y <- z;
            z+ 1;
            y;
        }
    };

    succ(n:Int) : AUTO_TYPE { n + 1};
};