-- Standar Cool Library
-- Some methods changed when building the ast to provide a python implementation for it
class Object {
    abort() : Object{
        self
    };
    
    type_name() : String {
        "Object"
    };
    
    copy() : SELF_TYPE {
        self    
    };
};

class String inherits Object {
    
    length() : Int { 0 };
    concat(s : String) : String { s };
    substr(i : Int, l : Int) : String { "string" };
};

class IO inherits Object {
    out_string(x : String) : SELF_TYPE { self };
    out_int(x : Int) : SELF_TYPE { self };
    in_string() : String { "string" };
    in_int() : Int { 0 };
};

class Int inherits Object { 
    abort() : Object{
        let io:IO <- new IO in {
            io.out_string("Abort called from class Int")
            @Object.abort();
        }
    };
    
    type_name() : String {
        "Int"
    };
};

class Bool inherits Object {
    abort() : Object{
        let io:IO <- new IO in {
            io.out_string("Abort called from class Bool")
            @Object.abort();
        }
    };
    
    type_name() : String {
        "Bool"
    };
 };

class Void { };