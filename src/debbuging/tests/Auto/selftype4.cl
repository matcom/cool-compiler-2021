--test2 es de tipo A asi que debe dar error xq A no confoma con SELF_TYPE de A

class Main inherits IO {
    main() : AUTO_TYPE {
		self 
	}; 
};

class A {
 	test:A <- self;
 	test2:SELF_TYPE <- test;
 };
 
 class B inherits A { };
 
