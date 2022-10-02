--Attributes are local to the class in which they are defined or inherited.

class A {
	a: Int <- 5;
	test(x1: Int, y1: Int): Int {
		let x: Int <- x1, y: Int <-y1 in {
			x <- "x + a";
			f <- y + a;
			if b then x + y else x - y fi;
		}
	};
};