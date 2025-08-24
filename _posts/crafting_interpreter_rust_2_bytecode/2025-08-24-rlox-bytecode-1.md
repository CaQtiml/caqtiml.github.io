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

This blog is not a rewritten version of [the original book](https://craftinginterpreters.com/contents.html). I only want to record the important things I need to know. This blog is more like my log book of what I should know and what I have done. You can use it as your guide too, but I apologize for my bad grammar and vocab choosing in advance. The full code can be found here (Give me a minute. I forget to make the repo public).

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