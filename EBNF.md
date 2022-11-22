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

Declaration = "Court", identifier, "(", [{define-type}], {[",", {define-type}]}, ")", ["->", type], Block

Program = (lambda | {Declaration})

Block = "{", {statement}, "}"

assignment = identifier, "=", RelExp, ";"

print = "Serve", "(" RelExp ")", ";"

while = "Deuce", "(" RelExp ")", statement

if-else = "In", "(" RelExp ")", statement, ["Out", statement]

return = "return", RelExp, ";"

statement = (lambda | assignment | funcall, ";" | print | define-type | while | Block | if-else | return)

RelExp = Expr, {("==" | "<" | ">" | "."), Expr}

Expr = Term, {("+" | "-" | "||"), Term}

Term = Factor, {("*" | "/" | "&&"), Factor}

variables = Relexp | ","

funccall = identifier, "(", [Relexp, [",", Relexp]] ")"

Factor = int | string | funccall | (("+" | "-" | "!" ), Factor) | ("(", RelExp, ")") | read

read = "Rally", "(", ")" 



