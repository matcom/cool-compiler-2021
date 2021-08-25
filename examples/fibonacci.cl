class Main inherits IO {
    fibonacci(n : Int) : Int {
         if n <= 2 then let x : Int <- 1 in x else let x : Int <- fibonacci(n - 1) + fibonacci(n - 2) in x fi
    };

    main() : Object {
    	let x : Int <- in_int() in out_int(fibonacci(x))
    };
};
