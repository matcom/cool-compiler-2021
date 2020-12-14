from run_pipeline import run_pipeline
from src.type_collector import TypeCollector
from src.type_builder import TypeBuilder
from src.type_checker import TypeChecker
from src.tset_builder import TSetBuilder
from src.tsets_reducer import TSetReducer
from src.tset_merger import TSetMerger
from src.cool_visitor import FormatVisitor

# Probando inferir los tipos de los parametros de un metodo a partir de los argumentos con los que se llama
# Se infiere:
# ---En el let de la clase Main ----
#   id : Int por la asignacion id <- self.in_int();
#   name : String por la asignacion name <- self.in_string();
#   email : String por la asignacion email <- self.in_string();
# --- En el metodo init() de la clase User---
#   id_ : Int porque en el llamado (new User).init(id, name, email) id es de tipo Int
#   name_ : String porque en el llamado (new User).init(id, name, email) name es de tipo String
#   email_ : String porque en el llamado (new User).init(id, name, email) email_ es de tipo String
#
def test():
    text = """
(* Testing IO *)
class Main inherits IO {

    main(): Object {
        let id: AUTO_TYPE, name: AUTO_TYPE, email: AUTO_TYPE in {
            out_string("Introduzca su id: ");
            id <- self.in_int();
            out_string("Introduzca su nombre: ");
            name <- self.in_string();
            out_string("Introduzca su email: ");
            email <- self.in_string();
            let user: AUTO_TYPE <- (new User).init(id, name, email) in
                out_string("Created user: ");
        }
    };
};

class User {
    id: AUTO_TYPE;
    name: AUTO_TYPE;
    email: AUTO_TYPE;

    init(id_: AUTO_TYPE, name_: AUTO_TYPE, email_: AUTO_TYPE): AUTO_TYPE { {
        id <- id_;
        name <- name_;
        email <- email_;
        self;
    } };

    get_name(): AUTO_TYPE {
        name
    };
};
       """

    ast = run_pipeline(text)
    errors = []

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    checker = TypeChecker(context, errors)
    checker.visit(ast, None)

    print(errors)
    if errors != []:
        print(errors)
        assert False

    tset_builder = TSetBuilder(context, errors)
    tset = tset_builder.visit(ast, None)

    tset_reducer = TSetReducer(context, errors)
    reduced_set = tset_reducer.visit(ast, tset)

    tset_merger = TSetMerger(context, errors)
    tset_merger.visit(ast, reduced_set)

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    checker = TypeChecker(context, errors)
    checker.visit(ast, None)

    formatter = FormatVisitor()
    tree = formatter.visit(ast)

    print("Errors:", errors)
    print("Context:")
    print(context)
    print(reduced_set)
    print(tree)

    assert errors == []
