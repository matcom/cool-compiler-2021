class Main inherits IO{
    a : Int <- 2;
    b : Int;
    c: Bool;
    main (): Object {
        {
            (* out_string(if not  a <= b then "True \n" else "False \n" fi); *)
            out_int(~a);
        }
    };
};
