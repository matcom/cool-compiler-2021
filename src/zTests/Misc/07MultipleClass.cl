class Main
{
	h:AUTO_TYPE <- new H;
	a:AUTO_TYPE <- new A;
	main(): Int 
	{
		{
			3;
		}
	};
};

class H
{
	a:Int;
};

class Z inherits H
{
	x:Int;
};

class A inherits F
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
