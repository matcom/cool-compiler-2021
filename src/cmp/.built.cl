class Object{
    abort() : Object { new Object };
    type_name() : String { "Object" };
    copy() : SELF_TYPE { new SELF_TYPE };
};

class IO{
    out_string(x: String): SELF_TYPE { new SELF_TYPE };
    out_int(x: Int): SELF_TYPE { new SELF_TYPE };
    in_string() : String { "" };
    in_int(): Int { 0 };
};

class Int{};

class String{
    length() : Int { 0 };
    concat(s : String) : String { "" };
    substr(i : Int, l : Int) : String { "" };
};

class Bool{};