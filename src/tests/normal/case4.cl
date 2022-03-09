class Main inherits IO {
    main(): Object
    {
			case new B of
				n : Object => 0;
				n : Bool => 1;
				n : Int => 2;
				n : String => 3;
				n : A => 4;
				n : B => 5;
				n : C => 6;
			esac
	}; 
};

class A { };

class B inherits A { };

class C inherits B { };
