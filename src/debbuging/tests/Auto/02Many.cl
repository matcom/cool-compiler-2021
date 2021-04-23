class Main inherits IO {
    a : AUTO_TYPE;
    b : AUTO_TYPE;
    c : AUTO_TYPE;
    d : AUTO_TYPE;
    main(n : AUTO_TYPE) : AUTO_TYPE {
		{
			a.a();
			b.a();
			c.a();
			d.a();
			b.b();
			c.b();
			d.b();
			c.c();
			d.c();
			d.d();
		}
	}; 
};

class A
{
    a() : SELF_TYPE
    {
    	self
    };
};

class B
{
    a() : SELF_TYPE
    {
    	self
    };
    b() : SELF_TYPE
    {
    	self
    };
};

class C
{
    a() : SELF_TYPE
    {
    	self
    };
    b() : SELF_TYPE
    {
    	self
    };
    c() : SELF_TYPE
    {
    	self
    } ;
};

class D
{
    a() : SELF_TYPE
    {
    	self
    };
    b() : SELF_TYPE
    {
    	self
    };
    c() : SELF_TYPE
    {
    	self
    };
    d() : SELF_TYPE
    {
    	self
    };
};

