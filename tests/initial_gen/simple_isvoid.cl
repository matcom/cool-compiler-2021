class Main inherits IO {
    a : IO;
    main() : AUTO_TYPE {
        let b: Bool <- isvoid a in
            if b then
                out_string("True")
            else
                out_string("False")
            fi
    };
};
