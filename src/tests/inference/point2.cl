class Main {
	step(p : AUTO_TYPE) : AUTO_TYPE 
	{
		p.translate(1,1)
	}; 
 
    main() : Object {
         let p : AUTO_TYPE <- new Point.init(0,0) in {
             step(p); -- Puede lanzar error semantico
         }
    };
};

class Point {
	x : AUTO_TYPE;
	y : AUTO_TYPE;
	translate(a:AUTO_TYPE, b:AUTO_TYPE) : AUTO_TYPE
	{
		{
			x <- a;
			y <- b;
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
