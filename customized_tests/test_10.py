from run_pipeline import run_pipeline
from src.type_collector import TypeCollector
from src.type_builder import TypeBuilder
from src.type_checker import TypeChecker
from src.tset_builder import TSetBuilder
from src.tsets_reducer import TSetReducer
from src.tset_merger import TSetMerger
from src.cool_visitor import FormatVisitor


def test():
    text = """
class Main inherits IO {
    main(): IO {
        let vector: AUTO_TYPE <- (new Vector2).init(0, 0) in
            vector.print_vector()
    };
};

class Vector2 {
    x: AUTO_TYPE;
    y: AUTO_TYPE;

    init(x_: AUTO_TYPE, y_: AUTO_TYPE): AUTO_TYPE { {
        x <- x_;
        y <- y_;
        self;
    } };


    get_x(): AUTO_TYPE {
        x
    };

    get_y(): AUTO_TYPE {
        y
    };

    add(v: Vector2): AUTO_TYPE {
        (new Vector2).init(x + v.get_x(), y + v.get_y())
    };

    print_vector(): AUTO_TYPE {
        let io: IO <- new IO in {
            io.out_string(" ( ");
            io.out_int(get_x());
            io.out_string("; ");
            io.out_int(get_y());
            io.out_string(" ) ");
        }
    };

    clone_vector(): AUTO_TYPE {
        (new Vector2).init(x, y)
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
