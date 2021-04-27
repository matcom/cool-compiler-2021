class Main {
	step(p : AUTO_TYPE) : AUTO_TYPE 
	{
		p.translate(1,1)
	}; 
 
    	main() : Int 
    	{
         let q : AUTO_TYPE <- new Point.init(0,0) in 
         	{
             		step(q);
         	}
    	};
};

class Point {
	x : AUTO_TYPE;
	y : AUTO_TYPE;
	translate(a:AUTO_TYPE, b:AUTO_TYPE) : AUTO_TYPE
	{
		{
			x <- a * b;
			y <- a + b;
		}
	};
	init(a:AUTO_TYPE, b:AUTO_TYPE) : AUTO_TYPE
	{
		{
			x <- a;
			y <- b;
			self;
		}
	};

};
