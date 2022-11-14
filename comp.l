%{
#include "comp.h"
%}

%%

"{"     return ABRECHAVE;
"}"     return FECHACHAVE;
"+"     return MAIS;
"-"     return MENOS;
"*"     return MULT;
"/"     return DIV;
"!"     return NOT;
"<"     return MENOR;
">"     return MAIOR;
"."     return CONCAT;
","     return VIRG;
":"     return DOISP;
"("     return PARENTESQ;
")"     return PARENTDIR;
";"     return PONTOEVIRGULA;
"||"    return OR;
"&&"    return AND;
"="     return IGUAL;
"=="    return IGUALIGUAL;
"""     return ASPAS;

"Serve"     return PRINT;
"Deuce"     return WHILE;
"In"        return IF;
"Out"       return ELSE;
"Rally"     return READ;
"Ace"       return VAR;
"String"    return STRING;
"int"       return INT;

[1-9][0-9]*     return NUM;
[a-zA-Z][a-zA-Z0-9_]*   return IDENTIFICADOR;
[a-zA-Z0-9!@#$%^&*()_\\-+=}[]{}:;,.?/`~]*   return STRINGVALUE;


%%

int yywrap(void){
    return 1;
}