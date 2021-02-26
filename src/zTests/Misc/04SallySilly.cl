class Silly 
{ 
	capy() : SELF_TYPE { self }; 
};
class Sally inherits Silly { };

class Main { 
	x : Sally <- (new Sally).capy();
	main() : Sally { x };
};