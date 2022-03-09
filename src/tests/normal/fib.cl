class Main inherits IO {
	main(): Main {
		out_int(fib(20))
	};
	fib(n : Int): Int {
		if n <= 1 then 1 else fib(n-1) + fib(n-2) fi 
	};
};
