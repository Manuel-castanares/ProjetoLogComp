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

Block   : ABRECHAVE

%%