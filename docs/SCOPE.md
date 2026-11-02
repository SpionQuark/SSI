## General idea:

Building a small programming language. SSI. 
What can SSI stand for? **S**uper **S**imple **I**dea.

The language should be learnable with ease, whilst still requiring you to employ basic programming techniques.

From feeling I'd build it rather as a OOP-language, though that might have to wait. It should also not require to be built. Making it an interpreted rather than compiled language makes useability better.

Running should work by using
```bash
ssi file.ssi
```

Written in Python (cause that is what I know)

> This document ``SCOPE.md`` just sets the scope for me
> for the next few weeks

### Types:
- numbers
- strings
- booleans
- lists

### Syntax:
- variables
- arithmetic
- comparisons
- ``if/else``
- ``while``
- ``for``
- functions with params
- return values
- comments being introduced with ``//`` as in Java
- ``{}`` like in Java
- ``()`` for parameters
- Statements must end with ``;``
- Leading ``.`` for numbers is rejected
- Leading ``0`` for numbers is allowed
- No multiline Strings, no escapes yet

### Built-Ins:
- ``print``
- ``len``
- ``input``

### Errors:
- Basic debugging behaviour

### File format:
- A code file end on ``.ssi``

## Build agenda:

1. **Lexer**: text in, token list out. Done when: `print("hi")` becomes the right tokens, with line numbers.
2. **Parser**: tokens in, syntax tree out. Done when: all syntax above parses, and bad input gives a syntax error.
3. **Interpreter**: runs the tree. Done when: variables, arithmetic, `if`, `while`, `for` work.
4. **Functions and scope**: parameters, return values, local variables.
5. **Errors and REPL**: line numbers in every error; a REPL for quick tests.
6. **Tests and examples**: a `tests/` folder with small programs and expected output; examples for FizzBuzz, a prime sieve, a guessing game.
7. **README**: syntax overview, install, five-minute tutorial.

## Definition of Build done:

Being able to build three test programs:
- HelloWorld
- FizzBuzz
- HigherLower