'''
[PROGRAM] ::= "package" [IDENTIFIER] [IMPORT_SECTION] [FUNC_SECTION]

[IMPORT_SECTION] ::= "import" [STRING] | ε

[FUNC_SECTION] ::= [FUNCTION] [FUNC_SECTION] | ε

[FUNCTION] ::= "func" [IDENTIFIER] "(" [PARAMS] ")" [BLOCK]

[PARAMS] ::= [PARAM] "," [PARAMS] | [PARAM] | ε

[PARAM] ::= [IDENTIFIER] [TYPE]

[TYPE] ::= "int" | "string"

[BLOCK] ::= "{" [STATEMENTS] "}"

[STATEMENTS] ::= [STATEMENT] [STATEMENTS'] | ε
[STATEMENTS'] ::= [STATEMENT] [STATEMENTS'] | ε

[STATEMENT] ::= [DECLARATION]  
              | [ASSIGNMENT]  
              | [RETURN_STATEMENT]  
              | [BLOCK]  
              | [METHOD_CALL]

[DECLARATION] ::= "var" [IDENTIFIER] [TYPE] "=" [EXPRESSION]

[ASSIGNMENT] ::= [IDENTIFIER] [ASSIGNMENT_OP] [EXPRESSION]  

[RETURN_STATEMENT] ::= "return" [EXPRESSION]

[EXPRESSION] ::= [TERM] [EXPRESSION']

[EXPRESSION'] ::= [ARITHMETIC_OP] [TERM] [EXPRESSION'] | ε

[TERM] ::= [FACTOR] [TERM']

[TERM'] ::= [ARITHMETIC_OP] [FACTOR] [TERM'] | ε

[FACTOR] ::= [IDENTIFIER] [FACTOR_TAIL] | [NUMBER] | [STRING] | "(" [EXPRESSION] ")" | [METHOD_CALL]

[FACTOR_TAIL] ::= "(" [ARGUMENTS] ")" | ε

[ARGUMENTS] ::= [EXPRESSION] "," [ARGUMENTS] | [EXPRESSION] | ε

[ARITHMETIC_OP] ::= "+" | "-" | "*" | "/" | "%"

[ASSIGNMENT_OP] ::= ":=" | "="

[IDENTIFIER] ::= "[a-zA-Z_][a-zA-Z0-9_]*"

[NUMBER] ::= "\d+(\.\d*)?"

[STRING] ::= "\"([^\"]|\\\")*\""

[QUALIFIED_IDENTIFIER] ::= [IDENTIFIER] "." [IDENTIFIER]

[METHOD_CALL] ::= [QUALIFIED_IDENTIFIER] "(" [ARGUMENTS] ")" | [IDENTIFIER] "(" [ARGUMENTS] ")"


'''