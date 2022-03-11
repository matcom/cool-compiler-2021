class Main inherits IO {
    boolop : BoolOp <- new BoolOp;
   main(): Object {

	let a:Int <- 0 ,line : String <- in_string() in
            while (boolop.and(not line="\n", not line.length()=1)) loop {
                a <- a+1;
        out_int(line.length());
		line <- in_string();

	    } pool
         
   };
};

class BoolOp {

  and(b1 : Bool, b2 : Bool) : Bool {
     if b1 then b2 else false fi
  };


};
