## EBNF Linguagem Tennis:

string = """, Letter, {Letter}, """

Letter = (A | B | C | ... | Z | a | b | c | ... | z)

int = Number, {Number}

Number = (0 | 1 | 2 | ... | 9)

special-symbols = symbols, {symbols}

symbols = (! | @ | # | $ | % | ^ | & | * | ( | ) | _ | - | + | = | { | } | [ | ] | : | ; | , | . | < | > | ? | /)

constant = string | int | special-symbols

type = "String" | "int"

identifier = Letter, {Letter | "_" | Number}

define-type = "ace", identifier, {","}, {identifier}, ":", type, ";"

Block = "{", {statement}, "}"

assignment = identifier, "=", RelExp, ";"

print = "Serve", "(" RelExp ")", ";"

while = "Deuce", "(" RelExp ")", statement

if-else = "In", "(" RelExp ")", statement, ["Out", statement]

statement = (lambda | assignment | print | define-type | while | Block | if-else)

RelExp = Expr, {("==" | "<" | ">" | "."), Expr}

Expr = Term, {("+" | "-" | "||"), Term}

Term = Factor, {("*" | "/" | "&&"), Factor}

Factor = int | string | (("+" | "-" | "!" ), Factor) | ("(", RelExp, ")") | read

read = "Rally", "(", ")" 



