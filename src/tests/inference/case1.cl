class Main inherits IO {
    main(): String
    {
    	"Kabuki"
    };
    
    test(a : AUTO_TYPE, b : AUTO_TYPE) : AUTO_TYPE {
		{
			if b then not b else a + 1 fi;
			case 3 + 5 of
				n : Bool => b;
				n : Int => not b;
				n : String => b;
			esac;
		}
	}; 
};
