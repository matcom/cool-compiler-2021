import ply.lex as lex
import tokens_rules

lexer = lex.lex(module=tokens_rules)


# To use the lexer, you first need to feed it some input text using its input() method. 
# After that, repeated calls to token() produce tokens. The following code shows how this
# works:


# Test it out
# data = '''
# 3 + 4 * 10
# + -20 *2
# '''

data = """
        class Cons inherits List{
            --class Cons super important comment
        xcar : Int ;
        xcdr : List ;
        ascommenterdnsideerdajajajaaquiiiedsacommentjajajaed(): Bool{true};
        isNill () : Bool{
                false};

        init (hd : Int, tl : List) : Cons{
                { xcar <- "hola \\t helou
                    sd";
                  xcdr <-  1 + 2;
                 self;}
        };
        };
        """

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1