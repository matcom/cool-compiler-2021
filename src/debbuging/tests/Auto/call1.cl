class Main inherits IO {
	main(): String
	{
		"Kabuki"
	};
    	test(x : AUTO_TYPE, y : AUTO_TYPE) : AUTO_TYPE {
		{
			if true then x.me() else y.myself() fi;
			x.he();
			if false then x else y fi;
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

class B inherits A {
	us():SELF_TYPE
		{
			self
		};
};

class C inherits B { };

class D inherits C { 
	they():SELF_TYPE
		{
			self
		};
};

class E inherits D { };


class F inherits C { };

class G inherits F {
	myself():SELF_TYPE
		{
			self
		};
 };

class H inherits G { };


class I{ 
	me():String
		{
			"Confusing"
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

class J inherits I { };

class K inherits J { };
