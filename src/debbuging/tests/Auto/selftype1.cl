--Error en B en el metodo test, se debe terminar con un self o new Self.

class Main inherits IO {
    main() : AUTO_TYPE {
		self 
	}; 
};

class A {
 	test(): SELF_TYPE {
 		new A
 	};
 	
 	test2(): SELF_TYPE {
 		new SELF_TYPE
 	};
 };
 
 class B inherits A { };
 
