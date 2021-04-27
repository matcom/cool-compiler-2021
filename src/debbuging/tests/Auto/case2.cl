(*
En este ejemplo se muestra como en la primera etapa de el inferenciador se maneja las ambiguedades en los Auto Types
*)

class Main inherits IO {
    main(a : AUTO_TYPE, b : AUTO_TYPE) : AUTO_TYPE {
		{
			if b then not b else a fi;
			case 3 + 5 of
				n : Bool => a.me();
				n : Int => 0;
				n : String => "Yay!";
			esac;
			a.you();
			a.she();
		}
	}; 
};

class A { 
	me():SELF_TYPE
		{
			self
		};
	you():SELF_TYPE
		{
			self
		};
	he():SELF_TYPE
		{
			self
		};
};
(*
class B inherits A { };

class C inherits B { };

class D inherits C { };

class E inherits D { };


class F inherits C { };

class G inherits F { };

class H inherits G { };
*)

class I{ 
	me():SELF_TYPE
		{
			self
		};
	you():SELF_TYPE
		{
			self
		};
	she():SELF_TYPE
		{
			self
		};
};
(*
class J inherits I { };

class K inherits J { };
*)
