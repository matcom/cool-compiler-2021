class Main inherits IO {
    main() : Object
    {
        let a : Int <- in_int(), b : Int <- in_int() in {
            if a < b then out_string("Menor\n") else out_string("Mayor(o igual, quien sabe)\n") fi;
        }
    };
};
