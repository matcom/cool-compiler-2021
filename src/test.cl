--The static types of the two sub-expressions must be Int.

class Main {
	a : AUTO_TYPE <- 12;
	hola(b: AUTO_TYPE): AUTO_TYPE {b};
	main(): Int {
		{
			hola(a);
		}
	};
};
