class Main inherits IO {
    main () : Object{
        let x : Object <- new SELF_TYPE in out_string(x.type_name().concat("\n"))
    };
};
