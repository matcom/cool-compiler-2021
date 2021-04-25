--SELF TYPE no se puede usar en los case

class Main inherits IO {
    main() : AUTO_TYPE {
		self 
	}; 
};

class A {
 	test(a:A): Int {
 		case a of
 		n:Int => 1;
 		n:Bool => 2;
 		n:SELF_TYPE => 4;
 		esac 
 	};
 };
 
 class B inherits A { };
 
