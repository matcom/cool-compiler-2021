--The static types of the two sub-expressions must be Int.

class Main {
	a : AUTO_TYPE <- 12;
	hola(b: Int): AUTO_TYPE {b};
	main(): Int {
		{
			hola(a);
			self;
		}
	};
};
