class Main inherits IO {
	a : A ;
    main(): Object
    {  
		{
			a <- (new B).f();
			out_string(a.type_name());
			
		}

	}; 
};

class A { f() : SELF_TYPE { new SELF_TYPE }; };

class B inherits A { };

class C inherits B { };
