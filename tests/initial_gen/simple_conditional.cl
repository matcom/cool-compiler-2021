class Main inherits IO {
    main() : IO {
        {
            if false then out_int(0) else out_int(1) fi;
            if true then out_int(0) else out_int(1) fi;
        }
    };
};