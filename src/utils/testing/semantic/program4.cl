class Main {
    a: Int;

    b: String;

    main () : String {{
        a = 0;
        b = "hola";
        function_with_errors();
    }};

    function_with_errors() : Object {
        case b of
            x: Int => (new IO).out_int(x);
            y: String => (new IO).out_string(y);
        esac
        
    };
};
