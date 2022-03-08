class Main inherits IO {
    msg : String <- "Hello World!\n";
    a : Int;
    b : Int;

    main() : IO {
        {
            self.out_string("Enter the first integer: ");
            a <- self.in_int();
            self.out_string("Enter the second integer: ");
            b <- self.in_int();
            self.out_string("The sum is: ");
            self.out_int(a + b);
            self.out_string("\n");
        }
    };
};