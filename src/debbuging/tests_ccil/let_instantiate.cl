 class Main inherits IO {
	main() : Main {
		let a : A  <- new A, b : B, c : Int <- 12 in 
			{  
				b <- a.f(); 
				c <- b.f(1,2);
				out_int(c); 
			} 
		};
	};

class A {
	f() : B {
	new B	
	};
};

class B {
	f(a : Int, b : Int) : Int {
	a + b
	};
};
