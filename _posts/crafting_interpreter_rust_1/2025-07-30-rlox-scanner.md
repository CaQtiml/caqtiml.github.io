---
title: 'Crafting Interpreters: A Tree-walk Interpreter in Rust - Part 1'
date: 2025-07-30
# permalink: /posts/2025/07/tree-walk-inter/
author_profile: false # set to false to not show your profile in this blog page.
excerpt: How I implement the tree-walk interpreter in Rust 
tags:
  - Rust
  - Tree-walk Interpreter
  - Crafting Interpreters
---

{% include toc %}

# Introduction

This blog is not a rewritten version of [the original book](https://craftinginterpreters.com/contents.html). I only want to record the important things I need to know. This blog is more like my log book of what I should know and what I have done. You can use it as your guide too, but I apologize for my bad grammar and vocab choosing in advance. The full code can be found [here](https://github.com/CaQtiml/rlox).

The brief roadmap
```
Source Code → Scanner → Tokens → Parser → AST → Interpreter → Result
    ↑                    ↑          ↑        ↑         ↑          ↑
"1 + 2 * 3"                                                     "7"
```

# Chapter 4: Scanning

Its purpose is to convert a script into tokens.

This is test.lox
```
var result = 10 + 5 * 2;
var flag = x != y and true;
```

It is scanned into 
```
Var var None
Identifier result None
Equal = None
Number 10 Some(Number(10.0))
Plus + None
Number 5 Some(Number(5.0))
Star * None
Number 2 Some(Number(2.0))
Semicolon ; None
Identifier flag None
Equal = None
Identifier x None
BangEqual != None
Identifier y None
And and None
True true Some(Boolean(true))
Semicolon ; None
Eof  None
```
Each line is each token of the script.

`Var var None` is a variable token. `Identifier result None` is an identifier token. And so on.

Each token shows a `TokenType`, `lexeme` that is the actual characters I used, and `literal` which is a literal value. For example `Number 2 Some(Number(2.0))` has a `TokenType` of `Number`, `lexeme` of `2`, and its literal value is `Some(Number(2.0))`.

A literal value is a value that appears directly in the source code - it's literally written there by the programmer. So literal value = "I know this value right now from the source code", but Value (in general) = "Some data that might be computed later", which will be evaluated from the literal value in the later chapter.

# Chapter 5: Representing Code

This chapter defines a grammar for Lox expressions and implements ASTs.
- Terminal symbol: A symbol that has a final value by itself, such as English alphabets.
- Non-terminal symbol: A symbol that refers to another rule in the grammar.

The grammar starts from 
```
expression     → literal
               | unary
               | binary
               | grouping ;

literal        → NUMBER | STRING | "true" | "false" | "nil" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
               | "+"  | "-"  | "*" | "/" ;
```

The AST is defined in `expr.rs`. For example, the syntax tree for a binary expression is as below.
```
Binary {
        left: Box<Expr>,
        operator: Token,
        right: Box<Expr>,
    },
```
For example, `1+2` becomes `Binary{left:1, operator:+, right:2}` (simplified form).

The example of a real AST is

```
let expression = Expr::binary(
        Expr::unary(
            Token::new(TokenType::Minus, "-".to_string(), None, 1),
            Expr::literal(Some(LiteralValue::Number(123.0))),
        ),
        Token::new(TokenType::Star, "*".to_string(), None, 1),
        Expr::grouping(Expr::literal(Some(LiteralValue::Number(45.67)))),
    );
```

which refers to the expression -123*(45.67)

```
let expression2 = Expr::binary(
        Expr::binary(
            Expr::literal(Some(LiteralValue::Number(1.0))),
            Token::new(TokenType::Plus, "+".to_string(), None, 1),
            Expr::literal(Some(LiteralValue::Number(2.0))),
        ),
        Token::new(TokenType::EqualEqual, "==".to_string(), None, 1),
        Expr::binary(
            Expr::literal(Some(LiteralValue::Number(4.0))),
            Token::new(TokenType::Minus, "-".to_string(), None, 1),
            Expr::literal(Some(LiteralValue::Number(3.0))),
        ),
    );
```
refers to (1+2) == (4-3).

This chapter concludes by implementing AST printer to convert `expression` to `(* (- 123) (group 45.67))`, convert `expression2` to `(== (+ 1 2) (- 4 3))`, and so on for other expressions. However, this is not useful yet. I now define AST, but I don't have a PARSER to convert from a list of tokens to AST yet.

The brief roadmap
```
Source Code → Scanner → Tokens → Parser → AST → Interpreter → Result
    ↑                    ↑          ↑        ↑         ↑          ↑
"1 + 2 * 3"          This chapter  Next     Later     Later    "7"
                    (representing  chapter  chapters  chapters
                     code)        (parsing) (eval)    (eval)
```

This chapter also covers a visitor pattern, but it will be written in another separated blog. 

# Chapter 6: Parsing Expressions

Problems: 
- After scanning, I have a flat list of tokens: `[NUMBER(1), PLUS(+), NUMBER(2), STAR(*), NUMBER(3)]`. However, how do I know that `1 + 2 * 3`, in the from of the token list, means `1 + (2 * 3)` and not `(1 + 2) * 3`?
- How do I handle 1 - 2 - 3? Left or Right Associative?
- How do I handle parentheses that override precedence?

The grammar in the previous chapter cannot solve this problem. I need to update it.

I use Recursive Descent, which is considered a top-down parser because it starts from the top or outermost grammar rule (here expression) and works its way down into the nested subexpressions before finally reaching the leaves of the syntax tree.

In a top-down parser, you reach the lowest-precedence expressions first because they may in turn contain subexpressions of higher precedence. So, I process from lower to higher precedence.

```
expression → equality ;
equality → comparison ( ( "!=" | "==" ) comparison )* ;
comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term → factor ( ( "-" | "+" ) factor )* ;
factor → unary ( ( "/" | "*" ) unary )* ;
unary → ( "!" | "-" ) unary | primary ;
primary → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
```

Briefly, this is how to convert these rules to Rust code. It is partially extracted from `parser.rs`.

```rust
pub struct Parser {
    tokens: Vec<Token>,
    current: usize, // point to the next token waiting to be parsed
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self {
            tokens,
            current: 0,
        }
    }

    pub fn parse(&mut self, error_reporter: &mut ErrorReporter) -> Option<Expr> {
        match self.expression() {
            Ok(expr) => Some(expr),
            Err(err) => {
                if let Some(parse_err) = err.downcast_ref::<ParseError>() {
                    error_reporter.report(parse_err.line, "", &parse_err.message);
                } else {
                    error_reporter.report(0, "", &err.to_string());
                }
                None // Return of Option when there is no value.
            }
        }
    }

    // Grammar rules - each becomes a method
    fn expression(&mut self) -> Result<Expr> {
        // TODO: Call equality()
        self.equality()
    }

    fn equality(&mut self) -> Result<Expr> {
        // TODO: Implement equality rule
        // Pattern: left-associative binary operators
        // Start with comparison(), then loop while I see != or ==
        let mut expr = self.comparison()?;

        while self.match_tokens(&[TokenType::BangEqual, TokenType::EqualEqual]) {
            let mut operator = self.previous().clone();
            let mut right_expr = self.comparison()?;
            expr = Expr::binary(expr, operator, right_expr);
        }
        Ok(expr) 
    }

    fn comparison(&mut self) -> Result<Expr> {
        // TODO: Similar to equality, but for >, >=, <, <=
        let mut expr = self.term()?;
        while self.match_tokens(&[TokenType::Greater, TokenType::GreaterEqual, TokenType::Less, TokenType::LessEqual]) {
            let mut operator = self.previous().clone();
            let right_expr = self.term()?;
            expr = Expr::binary(expr, operator, right_expr);
        }

        return Ok(expr);
    }
    ...
}
```

You see that each rule needs to use some helper functions such as `match_tokens(...)`, which also uses other helper functions. These helper functions main functionality is to let `current` field in the `parser` struct pointing to the current token in a token lists from `tokens` field. Some functions will also return a correct token to the grammar rule. For example
- `fn match_tokens(&mut self, types: &[TokenType]) -> bool` checks if the current token matches one of the `TokenType` list `types`. If yes, advance and return `true`. Otherwise, return `false`.
- `fn advance(&mut self) -> &Token` moves to next token and return the previous token.

Finally, this chapter transforms expression(s) to AST.
```
Testing Parser...

--- Testing: 1 + 2 * 3 ---
Result: (+ 1 (* 2 3)) // The result prints the AST in this format as I did in the previous chapter.

--- Testing: (1 + 2) * 3 ---
Result: (* (group (+ 1 2)) 3)

--- Testing: -123 * 45.67 ---
Result: (* (- 123) 45.67)

--- Testing: 1 == 2 != 3 ---
Result: (!= (== 1 2) 3)

--- Testing: !(1 < 2) ---
Result: (! (group (< 1 2)))

--- Testing: "hello" + "world" ---
Result: (+ hello world)

--- Testing: 1 + + 2 ---
[line 1] Error: Expect expression. at '+'
Parse failed (errors reported above)

--- Testing: (1 + 2 ---
[line 1] Error: Expect ')' after expression. at end
Parse failed (errors reported above)

--- Testing: * 5 ---
[line 1] Error: Expect expression. at '*'
Parse failed (errors reported above)
```

# Chapter 7: Evaluating Expressions

I now have an Abstract Syntax Tree (AST) that represents the expression structure; however, it is just data. It does not actually compute anything. I need to compute it! I write an interpreter `interpreter.rs` to do this work.

## LiteralValue vs Value
`LiteralValue` - Compile-Time Representation
- Represents literal values as they appear in source code
- Used during lexing and parsing phases
- Stored in tokens and AST nodes
- "What the programmer wrote"
- In a syntax world

`Value` - Runtime Representation
- Represents values during program execution
- Used during interpretation phase
- The actual computed results
- "What the program produces"
- in a mathematics world

Scanner Phase
```rust
// Lexer sees: "42" in source code
// Creates: Token with LiteralValue::Number(42.0)
self.add_token(TokenType::Number, Some(LiteralValue::Number(42.0)));
```

Parser Phase
```rust
// Parser builds AST node containing the LiteralValue
Expr::Literal { 
    value: Some(LiteralValue::Number(42.0))  // Still LiteralValue!
}
```

Interpreter Phase
```rust
// Interpreter converts LiteralValue to Value
fn visit_literal_expr(&mut self, _expr: &Expr, value: &Option<LiteralValue>) -> Result<Value> {
    match value {
        Some(LiteralValue::Number(n)) => Ok(Value::Number(*n)),  // Conversion!
        //   ^^^^^^^^^^^^^                   ^^^^^
        //   From AST                        To Runtime
    }
}
```

The Differences
- Lifecycle
    - LiteralValue: Born in lexer, dies in interpreter
    - Value: Born in interpreter, lives until program ends
    - `"42" → LiteralValue::Number(42.0) → Value::Number(42.0)`
- Mutability

```rust
// LiteralValue: Static, no operations
let lit = LiteralValue::Number(5.0);
// You can't do: lit + other_lit (no operators defined)

// Value: Dynamic, has operations  
let val = Value::Number(5.0);
val.is_truthy();
val.is_equal(&other_val);
```

## How visitor pattern is applied here
Use the visitor pattern to evaluate the expression by calling `.accept(...)`. This function peels one layer out and take the peeled expression to the accept function for further evaluation.

Briefly explaining why the visitor function is useful here.

There are several types of `Expr`, such as `Binary`, and `Unary`, and there are several operations we want from these `Expr`, such as printing the AST from `Expr` and evaluating `Expr` value. If we have to write everything in `expr.rs` under `impl Expr`, it will be very messy.

So, in `expr.rs`, I write general functions like `visit_binary_expr`, and `visit_unary_expr` and write `accept` function to check the `Expr` type from the `Expr` object and call the `visit_...` function that matches the `Expr` type. Then, I implement the behavior I want in a separate file. For example, If I want to print the `Expr` object, I implement the behavior of `visit_binary_expr` and `visit_unary_expr` to print the `Expr` object in `ast_printer.rs`. But if I want to evaluate the `Expr` object, I implement the behavior of `visit_binary_expr` and `visit_unary_expr` to evaluate the `Expr` object in `interpreter.rs`.

Then, how the program knows which `visit...` should be used? When we pass parameters to `accept` function, not only do I pass the `Expr` object, but I also pass the visitor object as well. The examples of the `visitor` object are `Interpreter` object and `AstPrinter` object. In `accept` function, it does like `visitor.visit_...(...)`. So, it uses `visit_...` from the object it receives.

In my code now,
- `Interpreter` object implements the `visit_...` function to evaluate the `Expr` object.
- `AstPrinter` object implements the `visit_...` function to print the `Expr` object.
The struct used to create the object that has `visit...` must implement `ExprVisitor`.
- `impl ExprVisitor<Result<Value>> for Interpreter {...}`
- `impl ExprVisitor<String> for AstPrinter {...}`

So, to summarize
- AST Printer: `ExprVisitor<String>` - converts tree to string representation
- Interpreter: `ExprVisitor<Result<Value>>` - converts tree to computed values
    - Calling `accept(...)` to `Interpreter` object evaluates the token.

For example
```rust
fn visit_unary_expr(&mut self, _expr: &Expr, operator: &Token, right: &Expr) -> Result<Value> {
    // TODO: Evaluate the right operand first, then apply the operator
    // Handle TokenType::Bang and TokenType::Minus
    // Remember to check types and throw runtime errors for invalid operations
    let mut right_value = right.accept(self)?; // Evaluate the Expr "right"
    match operator.token_type {
        TokenType::Bang => {
            Ok(Value::Boolean(!right_value.is_truthy()))
        },
        TokenType::Minus => {
            let num = self.check_number_operand(operator, &right_value)?;
            Ok(Value::Number(-num))
        },
        _ => Err(anyhow!("Unknown unary operator: {:?}", operator.token_type)),
    }
}
```

The reason I see the result of sth like `1+2` to be `3`, not `Value::Number(3.0)` because I implement `impl std::fmt::Display for Value` in `value.rs`.

So, in short, this chapter changes AST to the real value.

```
Testing Interpreter...

--- Evaluating: 1 + 2 ---
3

--- Evaluating: 3 * 4 - 2 ---
10

--- Evaluating: 10 / 2 ---
5

--- Evaluating: (1 + 2) * 3 ---
9

--- Evaluating: "hello" + " world" ---
hello world

--- Evaluating: "num: " + 42 ---
num: 42

--- Evaluating: true == false ---
false

--- Evaluating: !(5 > 3) ---
false

--- Evaluating: 3 >= 3 ---
true

--- Evaluating: nil == nil ---
true
```

Until now, I have finished this roadmap.
```
Source Code → Scanner → Tokens → Parser → AST → Interpreter → Result
    ↑                    ↑          ↑        ↑         ↑          ↑
"1 + 2 * 3"                                                     "7"
```
I have a statement, and I can write an interpreter to let it produce `7` for me. I will end this part here. The next part will be about making our language more like a language, not the calculator. Currently, my language cannot do sth like `var x=4;`, `if(x==1) ... else ...` yet. I need to extend the grammar to support these things.

# Grammar Summary
Chapter 5: Representing Code

```
expression     → literal
               | unary
               | binary
               | grouping ;

literal        → NUMBER | STRING | "true" | "false" | "nil" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
               | "+"  | "-"  | "*" | "/" ;
```

Chapter 6: Parsing Expression

```
expression → equality ;
equality → comparison ( ( "!=" | "==" ) comparison )* ;
comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term → factor ( ( "-" | "+" ) factor )* ;
factor → unary ( ( "/" | "*" ) unary )* ;
unary → ( "!" | "-" ) unary | primary ;
primary → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
```