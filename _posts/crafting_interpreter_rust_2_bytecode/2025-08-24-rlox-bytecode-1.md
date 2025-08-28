---
title: 'Crafting Interpreters: A Bytecode Virtual Machine in Rust - Part 1'
date: 2025-08-24
permalink: /posts/rlox-bytecode-1/
author_profile: false # set to false to not show your profile in this blog page.
excerpt: How I implement the bytecode virtual machine in Rust 
tags:
  - Rust
  - Bytecode Virtual Machine
  - Crafting Interpreters
---

{% include toc %}

# Introduction

This blog is not a rewritten version of [the original book](https://craftinginterpreters.com/contents.html). I only want to record the important things I need to know. This blog is more like my log book of what I should know and what I have done. You can use it as your guide too, but I apologize for my bad grammar and vocab choosing in advance. The full code can be found [here](https://github.com/CaQtiml/clox_rust).

My Learning Method
- I will ask LLM to generate a code skeleton with empty functions, and partial-filled struct and enum.
- I will try to fill them by myself by reading the chapters.

I am so certain that I can't implement everything from the scratch in the end since I use AI to generate the skeleton, but at least I am certain that I will understand essential concepts each chapter wants to teach.

This blog will be updated in parallel to my progress. So, this part is still underconstruction.

# Formatter for Reference

```rust
println!("{:8}", 42);      // "      42" (8 chars, space-padded)
println!("{:08}", 42);     // "00000042" (8 chars, zero-padded)
println!("{:<8}", 42);     // "42      " (8 chars, left-aligned)
println!("{:>8}", 42);     // "      42" (8 chars, right-aligned, same as default)
println!("{:^8}", 42);     // "   42   " (8 chars, center-aligned)
println!("{:08x}", 255);   // "000000ff" (8 chars, zero-padded hex)
```

# Chapter 1: Chunks of Bytecode

## Intended Result and Explanation
Let's start from the intended result of this chapter.

```rust
// test_helpers.rs

pub fn create_simple_chunk() -> Chunk {
    let mut chunk = Chunk::new();
    let c = chunk.add_constant(1.2); // c = 0 (first constant gets index 0)
    chunk.write_opcode(OpCode::Constant, 123); // Writes byte: 1. Append to `code` field in Chunk struct
    chunk.write(c as u8, 123); // Writes byte: 0. Append to `code` field in Chunk struct
    chunk.write_opcode(OpCode::Return, 123); // Writes byte: 0. Append to `code` field in Chunk struct
    chunk
}

pub fn verify_chunk_structure(chunk: &Chunk) {
    println!("Chunk Statistics:");
    println!("  Code size: {} bytes", chunk.count());
    println!("  Constants: {}", chunk.constants().count());
    println!("  Raw bytes: {:?}", chunk.code());
    println!();
}
```

When calling in `main()`,

```rust
fn main(){
    let chunk = create_simple_chunk();
    verify_chunk_structure(&chunk);
    disassemble_chunk(&chunk, "test chunk");
}
```
the result is

```
Chunk Statistics:
  Code size: 3 bytes
  Constants: 1
  Raw bytes: [1, 0, 0]

== test chunk ==
0000  123 OP_CONSTANT         0 '1.2'
0002    | OP_RETURN
```

First 2 bytes are from 

```rust
chunk.write_opcode(OpCode::Constant, 123);
chunk.write(c as u8, 123);
```
intended to declare a constant value 123, and the remaining 1 byte is from `chunk.write_opcode(OpCode::Return, 123);` that wants to return. Yes, just return. As a result, the code size is 3 bytes.

There is only 1 constant, which is 123. Make sense.

The raw bytes array `[1,0,0]` consisting of `[1,0]` from the constant declaring, and `[0]` from the return statement. The raw byte array consists of both opcode and index referring to a value in the `constants` field, which is an array, in `Chunk` struct. 

`[1,0]` for declaring 123 consists of `1`, which is an opcode for `Constant` (refer to `opcode.rs`), and `0`, which is an index to retrieve the actual value from the `constants` field.

`[0]` refers to opcode for `Return` (refer to `opcode.rs`).

To summarize

```
Offset | Byte | Meaning
-------|------|----------
0      | 1    | OP_CONSTANT opcode
1      | 0    | Constant index (operand for OP_CONSTANT)
2      | 0    | OP_RETURN opcode
```

For

```
== test chunk ==
0000  123 OP_CONSTANT         0 '1.2'
0002    | OP_RETURN
```

it is in the format `Byte Offset, Source Code Line Number, Instruction Name, Operand Value Index , Actual Operand Value accessing from Index`

To summarize,

```
Byte Array (code):
┌─────┬─────┬─────┐
│  1  │  0  │  0  │
└─────┴─────┴─────┘
  ↑     ↑     ↑
Offset: 0     1     2
        │     │     │
    OP_CONSTANT  Return
    opcode   operand opcode

Constants Array:
┌─────┐
│ 1.2 │  ← Index 0
└─────┘

Lines Array:
┌─────┬─────┬─────┐
│ 123 │ 123 │ 123 │
└─────┴─────┴─────┘
```

## Chunk Struct

```rust
pub struct Chunk {
    code: Vec<u8>, // The bytecode instructions
    constants: ValueArray, // Pool of literal values
    lines: Vec<usize>, // Line number of a particular bytecode
}
```

`code` stores the actual bytecode instructions that the virtual machine will execute. It contains opcodes (such as `Return` and `Constant`) and operands.

```
// For the Lox code: print 42;
// The bytecode might look like:
code: [1, 0, 0]  // [OP_CONSTANT, 0, OP_RETURN]
//      ^  ^  ^
//      |  |  └── Return instruction
//      |  └───── Constant index (operand)
//      └──────── Constant opcode
```

`Vec` gives us dynamic sizing, which ALMOST matches the book implementation. In fact, I should manage the memory by myself, but it involves `unsafe` feature, which I don't want to involve with now because I just start learning Rust.

`constants` stores literal values that appear in your source code.

```
// For Lox code like:
print 42;
print 3.14;

// The constants array would be:
constants: [42.0, 3.14]
//          idx 0, idx 1
```

The reasons we separate from the opcode

- Size flexibility: Values like strings or large numbers don't fit in a single byte.
- Managing a fixed-size instruction is a lot easier.

`lines` tracks which source code line each bytecode instruction came from.

```
// For Lox source:
// Line 10: var x = 42;
// Line 11: print x;

// Might compile to:
code:  [OP_CONSTANT, 0, OP_PRINT, OP_RETURN]
lines: [10,         10, 11,       11      ]
//      Each instruction remembers its source line
```

If the example .lox is

```
var a = 1.5;    // Line 1
var b = 2.8;    // Line 2  
print a + b;    // Line 3
```

the `Chunk` struct should be

```
Chunk {
    // The bytecode instructions
    code: [
        OP_CONSTANT, 0,  // Load 1.5 (constants[0])
        OP_CONSTANT, 1,  // Load 2.8 (constants[1]) 
        OP_ADD,          // Add them
        OP_PRINT,        // Print result
        OP_RETURN        // Return
    ],
    
    // The literal values
    constants: [
        1.5,  // idx 0
        2.8   // idx 1
    ],
    
    // Debug info - which source line each instruction came from
    lines: [
        1, 1,  // Constant, 0 came from line 1
        2, 2,  // Constant, 1 came from line 2
        3,     // Add came from line 3
        3,     // Print came from line 3
        3      // Return came from line 3
    ]
}
```

Analogy to Assembly Code

```
LOAD_CONST 0    ; Load constants[0] 
LOAD_CONST 1    ; Load constants[1]
ADD             ; Add top two stack values
PRINT           ; Print top of stack
RETURN          ; Exit
```

## ValueArray

In fact, a `ValueArray` struct can be eliminated and replaced by `Vec<Value>`. I have it to conform with the book style.

## Offset

In `simple_instruction`, it returns `offset+1` because the `return` opcode is 1 byte. So, moving 1 offset goes to the next bytecode.

In `constant_instruction`, it returns `offset+2` because the constant opcode is 2 bytes, including 1 byte for opcode and 1 byte for operand index. So, moving 2 offset goes to the next bytecode.

## write_opcode() and write_constant()

These are functions adding so that we don't have to manually cast the type in `main()` by ourself. Otherwise, in `main()`, we always need to do like

```rust
let constant = chunk.add_constant(1.2);
chunk.write(OpCode::Constant as u8, 123);
chunk.write(constant as u8, 123);
chunk.write(OpCode::Return as u8, 123);
```

With `write_opcode()`, we utilize `.into()` where its behavior is defined in `impl From<OpCode> for u8`.

## TryFrom and From Traits

The `TryFrom` trait is like a contract or interface. Rust provides the trait definition, but we need to provide the implementation for our specific types.

1. Rust provides the `Trait` definition.
2. We have to implement it for our type.

Imagine TryFrom is like a form template. Rust provides it for us.

```
CONVERSION FORM
From: _______ 
To: _______
How to convert: _____________
What if it fails: ___________
```
We need to fill it out.

```
CONVERSION FORM
From: u8
To: OpCode  
How to convert: match the byte value
What if it fails: return error message
```

In fact, the standard library provides some of them already.

```rust
// Standard library has these:
impl TryFrom<u32> for u8 { ... }        // u32 -> u8
impl TryFrom<i32> for u16 { ... }       // i32 -> u16
impl TryFrom<&str> for IpAddr { ... }   // String -> IP address
```

But in this chapter, we extend it.

```rust
impl TryFrom<u8> for OpCode { ... }
```

We are extending Rust's conversion system by telling it how to convert `u8` values into our custom `OpCode` type. We are not changing anything that already exists. We are adding a new capability.

Note that `TryFrom<u8> for OpCode` is One-Way only. Our implementation only handles `u8 → OpCode`. So, we need `From` trait to convert from OpCode to u8. You can think `From` trait as a template like `TryForm` as well.

We use `TryFrom` for `u8->OpCode` because not all `u8` have `OpCode`; however, all `OpCode` have `u8`, so we can use `From`.

# Chapter 2: A Virtual Machine

## Expected Output

```
=== Basic Constant Test ===
Chunk Statistics:
  Code size: 4 bytes
  Constants: 1
  Raw bytes: [1, 0, 2, 0]

--- Disassembly ---
== simple constant ==
0000  123 OP_CONSTANT         0 '1.2
'
0002    | OP_NEGATE
0003    | OP_RETURN
--- VM Execution ---

0000  123 OP_CONSTANT         0 '1.2
'
Loading constant: 1.2
          [ 1.2 ]
0002    | OP_NEGATE
-1.2
          [ -1.2 ]
0003    | OP_RETURN
-1.2

✓ Execution completed successfully

=== Arithmetic Test: -(1.2 + 3.4) ===
Chunk Statistics:
  Code size: 7 bytes
  Constants: 2
  Raw bytes: [1, 0, 1, 1, 3, 2, 0]

--- Disassembly ---
== arithmetic test ==
0000  123 OP_CONSTANT         0 '1.2
'
0002    | OP_CONSTANT         1 '3.4
'
0004    | OP_ADD
0005    | OP_NEGATE
0006    | OP_RETURN
--- VM Execution ---

0000  123 OP_CONSTANT         0 '1.2
'
Loading constant: 1.2
          [ 1.2 ]
0002    | OP_CONSTANT         1 '3.4
'
Loading constant: 3.4
          [ 1.2 ][ 3.4 ]
0004    | OP_ADD
          [ 4.6 ]
0005    | OP_NEGATE
-4.6
          [ -4.6 ]
0006    | OP_RETURN
-4.6

✓ Execution completed successfully

=== Complex Arithmetic Test: ((1 + 2) * 3 - 4)/4 ===
Chunk Statistics:
  Code size: 15 bytes
  Constants: 5
  Raw bytes: [1, 0, 1, 1, 3, 1, 2, 5, 1, 3, 4, 1, 4, 6, 0]

--- Disassembly ---
== complex arithmetic ==
0000  123 OP_CONSTANT         0 '1
'
0002    | OP_CONSTANT         1 '2
'
0004    | OP_ADD
0005    | OP_CONSTANT         2 '3
'
0007    | OP_MULTIPLY
0008    | OP_CONSTANT         3 '4
'
0010    | OP_SUBTRACT
0011    | OP_CONSTANT         4 '4
'
0013    | OP_DIVIDE
0014    | OP_RETURN
--- VM Execution ---

0000  123 OP_CONSTANT         0 '1
'
Loading constant: 1
          [ 1 ]
0002    | OP_CONSTANT         1 '2
'
Loading constant: 2
          [ 1 ][ 2 ]
0004    | OP_ADD
          [ 3 ]
0005    | OP_CONSTANT         2 '3
'
Loading constant: 3
          [ 3 ][ 3 ]
0007    | OP_MULTIPLY
          [ 9 ]
0008    | OP_CONSTANT         3 '4
'
Loading constant: 4
          [ 9 ][ 4 ]
0010    | OP_SUBTRACT
          [ 5 ]
0011    | OP_CONSTANT         4 '4
'
Loading constant: 4
          [ 5 ][ 4 ]
0013    | OP_DIVIDE
          [ 1.25 ]
0014    | OP_RETURN
1.25

✓ Execution completed successfully
```

## Different Ways to Handle Errors in anyhow

- `bail`: Immediate error return. Use when
    - We want a simple validation
    - Early Exit from functions

```rust
fn divide(a: f64, b: f64) -> Result<f64> {
    if b == 0.0 {
        bail!("Cannot divide by zero"); // Also return Err() for us.
    }
    Ok(a / b)
}
```

- `anyhow`: Create Error without returning. Use when
    - We want to store the error for later use
    - We need to do something else before returning

```rust
fn validate_input(x: i32) -> Result<i32> {
    if x < 0 {
        let error = anyhow::anyhow!("Negative input: {}", x);
        return Err(error); // We still need this line to return an error
    }
    Ok(x * 2)
}
```

## as_ref

For `let chunk = self.chunk.as_ref().expect("No chunk loaded");`, `as_ref` changes from `Option<Chunk>` to `Option<&Chunk>` so that `.expect()` unwraps to get `&Chunk`, which is a variable borrowing instead of taking an ownership.

If we do `let chunk = self.chunk.expect("No chunk loaded");`, it takes OWNERSHIP and DESTROY `self.chunk`.

# Chapter 3: Scanning on Demand

<!-- I will come back later. I cheat now by asking LLM to generate me a full scanner code so that I can do the next chapter. Sorry, I feel it is redundant to this chapter in Tree-walking interpreter. -->

## Expected Result

Giving this .lox script

```
// This is a comment
print "Hello, world!";
var x = 123.45;
if (x > 100) {
    print "Large number: " + x;
}

for (var i = 0; i < 5; i = i + 1) {
    print i;
}
```

This is an expected output.

```
   2 31 'print'
   | 20 '"Hello, world!"'
   |  8 ';'
   3 36 'var'
   | 19 'x'
   | 13 '='
   | 21 '123.45'
   |  8 ';'
   4 28 'if'
   |  0 '('
   | 19 'x'
   | 15 '>'
   | 21 '100'
   |  1 ')'
   |  2 '{'
   5 31 'print'
   | 20 '"Large number: "'
   |  7 '+'
   | 19 'x'
   |  8 ';'
   6  3 '}'
   8 26 'for'
   |  0 '('
   | 36 'var'
   | 19 'i'
   | 13 '='
   | 21 '0'
   |  8 ';'
   | 19 'i'
   | 17 '<'
   | 21 '5'
   |  8 ';'
   | 19 'i'
   | 13 '='
   | 19 'i'
   |  7 '+'
   | 21 '1'
   |  1 ')'
   |  2 '{'
   9 31 'print'
   | 19 'i'
   |  8 ';'
  10  3 '}'
   | 39 ''
```

This is a compile code `compiler.rs`. It is provided here as a reference of how to use each token.

```rust
pub fn compile(source: String) {
    let mut scanner = Scanner::new(source);
    let mut line = 0;
    
    loop {
        let token = scanner.scan_token();
        
        if token.line != line {
            print!("{:4} ", token.line);
            line = token.line;
        } else {
            print!("   | ");
        }
        
        println!("{:2} '{}'", token.token_type as u8, token.lexeme);
        
        if token.token_type == TokenType::Eof {
            break;
        }
    }
}
```

## TokenType to u8

```rust
println!("{:2} '{}'", token.token_type as u8, token.lexeme);
```

The `as u8` is doing a type cast that converts the enum variant into its underlying numeric representation. In Rust, enums have hidden numeric values called "discriminants". By default, they start at 0 and increment.

```rust
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TokenType {
    // Single-character tokens
    LeftParen,    // = 0
    RightParen,   // = 1
    LeftBrace,    // = 2
    RightBrace,   // = 3
    Comma,        // = 4
    Dot,          // = 5
    Minus,        // = 6
    Plus,         // = 7
    Semicolon,    // = 8
    Slash,        // = 9
    Star,         // = 10
    
    // One or two character tokens
    Bang,         // = 11
    BangEqual,    // = 12
    Equal,        // = 13
    EqualEqual,   // = 14
    Greater,      // = 15
    GreaterEqual, // = 16
    Less,         // = 17
    LessEqual,    // = 18
    
    // Literals
    Identifier,   // = 19
    String,       // = 20
    Number,       // = 21
    
    // Keywords
    And,          // = 22
    Class,        // = 23
    // ... and so on
}
```

You can also set the custom values.

```rust
#[repr(u8)]  // This ensures it uses u8 as the underlying type
pub enum TokenType {
    // Single-character tokens
    LeftParen = 0,
    RightParen = 1,
    LeftBrace = 2,
    // ... etc
    
    // Or skip around:
    String = 20,
    Number = 21,
    Print = 31,
    Eof = 39,
}
```

It is also possible to print the enum name directly.

```rust
println!("{:12} '{}'", format!("{:?}", token.token_type), token.lexeme);
```
## Token and Scanner Struct

We have covered this once in the tree-walk interpreter, but let's review here again quickly/

```rust
#[derive(Debug, Clone)]
pub struct Token {
    pub token_type: TokenType,
    pub lexeme: String,
    pub line: usize,
}
```

Each token shows a `TokenType`, `lexeme` that is the actual characters I used, and `literal` which is a literal value. For example `Number 2 Some(Number(2.0))` has a `TokenType` of `Number`, `lexeme` of `2`, and its literal value is `Some(Number(2.0))`.

```rust
pub struct Scanner {
    source: String, // In fact, unused. To be removed later.
    chars: Vec<char>, // The vector of source code's character
    start: usize, // Start of current token being scanned
    // Example: When scanning "print", start points to 'p'
    current: usize, // Current position in the source
    line: usize, // Current line number -> For error reporting
}
```

Example

- `chars: Vec<char>`  For source `print 42;`, this becomes `['p', 'r', 'i', 'n', 't', ' ', '4', '2', ';']`
- `start: usize` When scanning `print`, start points to `p`
- `current: usize` While scanning `print`, current moves from `'p' → 'r' → 'i' → 'n' → 't' → ' '`
- `line: usize` Incremented every time we encounter a `'\n'` character

Let's trace through scanning the token `print` from source code `print 42;`

```
Source: p r i n t   4 2 ;
Index:  0 1 2 3 4 5 6 7 8

Initial state:
start: 0, current: 0    // Both point to 'p'
        ↓
        p r i n t   4 2 ;

After scanning "print":
start: 0, current: 5    // start at 'p', current at ' '
        ↓         ↓
        p r i n t   4 2 ;
        └─────────┘
        This is our token lexeme
```

Full Example

```
Token 1: "var"
├─ start: 0, current: 0 → 3
├─ lexeme: chars[0..3] = "var"
└─ line: 1

Token 2: "x"  
├─ start: 4, current: 4 → 5
├─ lexeme: chars[4..5] = "x"
└─ line: 1

Token 3: "="
├─ start: 6, current: 6 → 7  
├─ lexeme: chars[6..7] = "="
└─ line: 1
```

# Chapter 4: Compiling Expressions

## How to Print Debug

Uncomment `self.debug_trace_execution();` in `fn run(&mut self) -> Result<InterpretResult>` in `vm.rs`.

## 'static lifetime

`'static` is a lifetime annotation in Rust. It means the data lives for the entire duration of the program. It is the longest possible lifetime in Rust.

```rust
fn get_rule(token_type: TokenType) -> &'static ParseRule {
    match token_type {
        TokenType::LeftParen => &ParseRule { 
            prefix: Some(Compiler::grouping), 
            infix: None, 
            precedence: Precedence::None 
        },
        // ... more rules
    }
}
```

`ParseRule` created in each match arm is temporary and destroyed when the function returns. `'static` tells Rust that these `ParseRule` structs should live forever, so it is safe to return references to them as borrowing.

Behind the scene is that when **compiling**, Rust puts these `ParseRule` structs in the program's static memory. Review the OS process layout if you already forget. It is in the "Data" section, which is the same place as the global variable. It is **NOT in the heap**. It is **NOT LATER MOVED** from stack section to the data section.

```
┌─────────────────┐
│   Stack         │ ← Local variables (dies when function ends)
├─────────────────┤
│   Heap          │ ← Dynamic allocations (Box, Vec, String)
├─────────────────┤
│   Static Memory │ ← 'static data lives here! (never dies)
├─────────────────┤
│   Program Code  │ ← Your compiled functions
└─────────────────┘
```

Let's review a bit.

- Stack: dies when the function ends.

```rust
fn broken() -> &ParseRule {  // No 'static
    let rule = ParseRule { /* ... */ };  // Lives on stack
    &rule  // ERROR: rule dies when function ends!
}
```

- Heap: Manual Memory Management, which is unrelated in this scenario

```rust
fn heap_version() -> Box<ParseRule> {  // Ownership transfer
    Box::new(ParseRule { /* ... */ })  // Allocated on heap
    // Caller now owns this and must eventually drop it
}
```

- Static Memory

```rust
fn static_version() -> &'static ParseRule {
    &ParseRule { /* ... */ }  // Rust puts this in static memory
    // Lives for entire program duration
}
```

If you want to avoid using `'static`, you need to return owned objects instead.

```rust
fn get_rule(token_type: TokenType) -> ParseRule {  // Returns owned object
    ParseRule { /* ... */ }  // No & here!
}
```

## Grammar

The grammar starts from this. It is taken from tree-walk interpreter [Ch5](/posts/rlox-tree-1/#grammar-summary).

```
expression → equality ;
equality → comparison ( ( "!=" | "==" ) comparison )* ;
comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term → factor ( ( "-" | "+" ) factor )* ;
factor → unary ( ( "/" | "*" ) unary )* ;
unary → ( "!" | "-" ) unary | primary ;
primary → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
```

## parse_precedence, get_rule, and Pratt Parsing

This is the most important part of this chapter. `parse_precedence` takes a minimum precedence level and says that "Parse an expression, but only consume operators that have at least this precedence level."

```rust

fn get_rule(token_type: TokenType) -> &'static ParseRule {
    use TokenType::*;
    match token_type {
        LeftParen => &ParseRule { 
            prefix: Some(Compiler::grouping),   // Left Paren can be a prefix by behaving as grouping. 
            infix: None,                        // It can't be an infix.
            precedence: Precedence::None 
        },
        Number => &ParseRule { 
            prefix: Some(Compiler::number), 
            infix: None, 
            precedence: Precedence::None 
        },
        Minus => &ParseRule { 
            prefix: Some(Compiler::unary),  // You can see -1
            infix: Some(Compiler::binary),  // You can see ... - ...
            precedence: Precedence::Term    // Minus has a precedence of "Term"
        },
        Plus => &ParseRule { 
            prefix: None, 
            infix: Some(Compiler::binary), 
            precedence: Precedence::Term    // Plus has a precedence of "Term" 
        },
        Star => &ParseRule { 
            prefix: None, 
            infix: Some(Compiler::binary), 
            precedence: Precedence::Factor  // Star has a precedence of "Factor" 
        },
        Slash => &ParseRule { 
            prefix: None, 
            infix: Some(Compiler::binary), 
            precedence: Precedence::Factor  // Slash has a precedence of "Factor" 
        },
        _ => &ParseRule { 
            prefix: None, 
            infix: None, 
            precedence: Precedence::None 
        },
    }
}

fn parse_precedence(&mut self, precedence: Precedence) {
        // This is the core of Pratt parsing!
        // 1. Advance and get the prefix rule for the current token
        self.advance();
        // 2. Call the prefix function
        let prefix_rule = Self::get_rule(self.parser.previous.token_type).prefix;
        
        match prefix_rule {
            Some(prefix_fn) => prefix_fn(self),
            None => {
                self.error("Expect expression.");
                return;
            }
        }
        // 3. While we have infix operators with higher precedence:
        //    - Get the infix rule and call the infix function
        while precedence <= Self::get_rule(self.parser.current.token_type).precedence {
            self.advance();
            let infix_rule = Self::get_rule(self.parser.previous.token_type).infix;
            if let Some(infix_fn) = infix_rule {
                infix_fn(self);
            }
        }
    }
```

- Example 1: Simple Number `42`

```
Input: "42"
Call: parse_precedence(Assignment)  // Assignment = precedence 1

Step 1: advance() -> previous = "42"
Step 2: get prefix rule for Number -> calls number()
Step 3: number() emits: CONSTANT 42
Step 4: while loop condition: Assignment(1) <= precedence of EOF(None=0)? 
        -> 1 <= 0? NO, exit loop
Result: Just loads constant 42 (Write to a sequence of bytecode)
```

- Example 2: Simple Number `-42`

```
Input: "-42"
Call: parse_precedence(Assignment)  // precedence = 1

Step 1: advance() -> previous = "-", current = "42"     --------- FIRST move from "-" to "42"
Step 2: get prefix rule for Minus -> calls unary()
Step 3: unary() does:
    a. operator_type = Minus (save the operator)
    b. calls parse_precedence(Unary) = parse_precedence(8)
    
    Recursive call parse_precedence(Unary=8):
    - advance() -> previous = "42", current = EOF     --------- SECOND move from "42" to "EOF"
    - get prefix rule for Number -> calls number()
    - number() emits: CONSTANT 42
    - while check: Unary(8) <= precedence of EOF(0)? 
      -> 8 <= 0? NO, return to unary()
    
    c. unary() emits: NEGATE

Step 4: Back in original parse_precedence(Assignment=1):
        while check: Assignment(1) <= precedence of EOF(0)?
        -> 1 <= 0? NO, exit

Result: CONSTANT 42, NEGATE 

VM will compile this result and give -42 as a result. Review Ch2 if you feel confused.
```

- Example 3: Simple Addition `1+2`

```
Input: "1 + 2"
Call: parse_precedence(Assignment)  // precedence = 1

Step 1: advance() -> previous = "1"     ------------------------------------------- FIRST move
Step 2: get prefix rule for Number -> calls number()
Step 3: number() emits: CONSTANT 1

Step 4: while loop check: Assignment(1) <= precedence of "+"(Term=6)?
        -> 1 <= 6? YES, continue loop

Step 5: advance() -> previous = "+"     ------------------------------------------- SECOND move
Step 6: get infix rule for Plus -> calls binary()
Step 7: binary() does:
        - operator_type = Plus
        - calls parse_precedence(Term.next()) = parse_precedence(Factor=7)
        
        Recursive call parse_precedence(Factor=7):
        - advance() -> previous = "2"       --------------------------------------- THIRD move
        - number() emits: CONSTANT 2
        - while check: Factor(7) <= precedence of EOF(0)? NO, return
        
Step 8: binary() emits: ADD

Step 9: while check: Assignment(1) <= precedence of EOF(0)? NO, exit

Result: CONSTANT 1, CONSTANT 2, ADD
```

- Example 4: Mixed Precedence `1+2*3`

```
Input: "1 + 2 * 3"
Call: parse_precedence(Assignment)  // precedence = 1

Step 1-3: Parse "1", emit CONSTANT 1

Step 4: while check: Assignment(1) <= precedence of "+"(Term=6)? YES

Step 5-6: advance() to "+", call binary()
Step 7: binary() calls parse_precedence(Factor=7) for right side

    Recursive call parse_precedence(Factor=7):
    - advance() -> previous = "2"
    - number() emits: CONSTANT 2
    
    - while check: Factor(7) <= precedence of "*"(Factor=7)? YES
    - advance() -> previous = "*"
    - binary() calls parse_precedence(Unary=8)
    
        Deeper recursive call parse_precedence(Unary=8):
        - advance() -> previous = "3"
        - number() emits: CONSTANT 3
        - while check: Unary(8) <= precedence of EOF(0)? NO, return
        
    - binary() emits: MULTIPLY
    - while check: Factor(7) <= precedence of EOF(0)? NO, return

Step 8: binary() emits: ADD

Result: CONSTANT 1, CONSTANT 2, CONSTANT 3, MULTIPLY, ADD
```

For the fourth example, don't forget that this is a stack-based VM. The execution step will be

1. CONSTANT 1, CONSTANT 2, CONSTANT 3, MULTIPLY, ADD
2. CONSTANT 1, CONSTANT 6, ADD
3. CONSTANT 7

## .next() in Binary

It implements left associativity.

For `1 + 2 + 3`:

- First `+` calls `parse_precedence(Factor=7)` for its right side
- When parsing `2`, we see another `+` (Term=6)
- Check: Factor(7) <= Term(6)? NO! So we don't consume the second `+`
- This forces the parsing to be: `(1 + 2) + 3` instead of `1 + (2 + 3)`

```
1 + 2 * 3

Low precedence call (Assignment=1):
"I'll take anything!"
├─ parse "1" 
├─ see "+" (precedence 6 >= 1) ✓ take it!
│  └─ High precedence call (Factor=7) for right side:
│     "I only want high-precedence stuff!"
│     ├─ parse "2"
│     ├─ see "*" (precedence 7 >= 7) ✓ take it!
│     │  └─ Very high precedence call (Unary=8):
│     │     ├─ parse "3" 
│     │     └─ see EOF (precedence 0 < 8) ✗ stop
│     └─ emit MULTIPLY
└─ emit ADD
```

Higher precedence operations naturally get parsed deeper in the recursion, which means they execute first when the stack unwinds!