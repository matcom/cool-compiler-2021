class Main {
    main (): Object {
        0
    };

    f(): AUTO_TYPE {
        if true then
            if true then
                create_dog()
            else
                create_cat() fi
        else
            create_reptile() fi
    };

    create_dog(): AUTO_TYPE {
        new Dog
    };

    create_cat(): AUTO_TYPE {
        new Cat
    };

    create_reptile(): AUTO_TYPE {
        new Reptile
    };
}

class Animal {}
class Mammal inherits Animal {}
class Reptile inherits Animal {}
class Dog inherits Mammal {}
class Cat inherits Mammal {}