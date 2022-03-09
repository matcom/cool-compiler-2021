class Main
{
	h:AUTO_TYPE <- new A;
	a:AUTO_TYPE <- new D;
	main(): Int 
	{
		{
			3;
		}
	};
};


class A
{
	b:Int;
};

class B inherits A
{
	c:Int;
};

class C inherits B
{
	e:Int;
};

class D inherits C
{
	f:Int;
};

class F inherits D
{
	g:Int;
};
