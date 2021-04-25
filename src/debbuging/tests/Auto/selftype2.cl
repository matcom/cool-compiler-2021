--SELF TYPE no se puede usar como parametro

class Main inherits IO {
    main() : AUTO_TYPE {
		self 
	}; 
};

class A {
 	test(b:SELF_TYPE): SELF_TYPE {
 		b
 	};
 	test2(): SELF_TYPE {
 		let b:SELF_TYPE in b
 	};
 };
 
 class B inherits A { };
 
