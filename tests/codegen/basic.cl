class Main inherits IO {
   a : String <- "Hello world\n";
   main(): IO {
      let b : Int <- 0, c : Bool <- false in out_string(a)
   };
};

--class Main inherits IO {
--   main(): IO {
--      out_int(f())
--   };
--   f() : Int {
--      if true then
--        1
--      else
--        2
--      fi
--   };
--};