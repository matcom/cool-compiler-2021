class Main {
     main() : Int { 0 };

     method0( a : AUTO_TYPE) : AUTO_TYPE {
         {
             a.method(a);
             a;
         }
     };

};

class A {
    method(a : AUTO_TYPE): AUTO_TYPE { a }; 
};

class B inherits A {
    method(b : AUTO_TYPE) : AUTO_TYPE { b };
};