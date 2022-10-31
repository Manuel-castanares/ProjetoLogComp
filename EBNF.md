## EBNF Linguagem Tennis:

### Tipos:

string = Letter, {Letter}

Letter = A | B | C | ... | Z | a | b | c | ... | z

int = Number, {Number}

Number = 0 | 1 | 2 | ... | 9

constante = string | int

tipo = "String" | "int"

identificador = Letter, {Letter | "_" | Number}

definição-tipo = "var" identificador ":" tipo {"=" constante} ";"

definição-tipo-multivar = "var" identificador "," {identificador} ":" tipo ";"
