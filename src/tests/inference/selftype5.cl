--Que pasa en test. Su expresion es del tipo A, o del tipo SELF_TYPE

class Main inherits IO {
    main() : AUTO_TYPE {
		self 
	}; 
};

class A inherits IO {
	v:String;
 	test(): SELF_TYPE
 	{
 		new SELF_TYPE.out_string(v)
 	};
 };
 
 class B inherits A { };
 
