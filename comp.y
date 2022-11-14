%{

%}

%start Init
%token ABRECHAVE
%token FECHACHAVE
%token MAIS
%token MENOS
%token MULT
%token DIV
%token NOT
%token MENOR
%token MAIOR
%token CONCAT
%token VIRG
%token DOISP
%token PARENTESQ
%token PARENTDIR
%token PONTOEVIRGULA
%token OR
%token AND
%token IGUAL
%token IGUALIGUAL
%token ASPAS
%token PRINT
%token WHILE
%token IF
%token ELSE
%token READ
%token VAR
%token STRING
%token INT
%token NUM
%token IDENTIFICADOR
%token STRINGVALUE
%token FUNCTION
%token RETURN

%%
Init    : FUNCT Init
        | Block
        ;

FUNCT   : FUNCTION IDENTIFICADOR PARENTESQ PARAMETROS PARENTDIR ABRECHAVE STATEMENTS RETURN DEVOLUCAO PONTOEVIRGULA FECHACHAVE
        ;

DEVOLUCAO   : 
            | STRINGVALUE
            | NUM
            ;

STATEMENTS  : 
            | statement
            | statement STATEMENTS
            ;

PARAMETROS  : 
            | IDENTIFICADOR
            | VIRGULA IDENTIFICADOR PARAMETROS
            ;

Block   : ABRECHAVE DENTRO FECHACHAVE
        ;

DENTRO  : STATEMENTS
        ;

statement   : PONTOEVIRGULA
            | IDENTIFICADOR IGUAL RELEXP PONTOEVIRGULA
            | PRINT PARENTESQ RELEXP PARENTDIR PONTOEVIRGULA
            | VAR PARAMETROS DOISP TIPO PONTOEVIRGULA
            | WHILE PARENTESQ RELEXP PARENTDIR statement
            | Block
            | if-else
            ;

if-else     : IF PARENTESQ RELEXP PARENTDIR statement else
            ;

else        : 
            | statement
            ;

TIPO    : INT
        | STRING
        ;

RELEXP  : EXPR
        | EXPR OPERACOESRELEXP RELEXP
        ;

OPERACOESRELEXP     : IGUALIGUAL
                    | MENOR
                    | MAIOR
                    | CONCAT
                    ;

EXPR    : TERM
        | TERM OPERACOESEXPR EXPR
        ;

OPERACOESEXPR   : MAIS
                | MENOS
                | OR
                ;

TERM    : FACTOR
        | FACTOR OPERACOESTERM TERM
        ;

OPERACOESTERM   : MULT
                | DIV
                | AND
                ;

FACTOR  : NUM
        | STRINGVALUE
        | IDENTIFICADOR
        | BINOPS FACTOR
        | PARENTESQ RELEXP PARENTDIR
        | READ PARENTESQ PARENTDIR
        ; 

BINOPS  : MAIS
        | MENOS
        | NOT
        ; 

%%

int main(void){
    return yyparse();
}