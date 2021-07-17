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
(* This program prints the first 10 numbers of fibonacci *)
class Main {

    main(): Object {
        let total: AUTO_TYPE <- 10,
            i: AUTO_TYPE <- 1 ,
            io: AUTO_TYPE <- new IO in
                while i <= total loop {
                    io.out_int(fibonacci(i));
                    io.out_string("n");
                    i <- i + 1;
                }
                pool
    };

    fibonacci (n: AUTO_TYPE): AUTO_TYPE {
        if n <= 2 then 1 else fibonacci(n - 1) + fibonacci(n - 2) fi
    };
};        """

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
