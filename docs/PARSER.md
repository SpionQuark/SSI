# Parser Build Docs

So, as far as I understand the parser, he turns the tokens we get from ``Lexer(<code>).tokenize()`` into the running code with which our coding language
is built. So, the Parser must translate the tokens of the SSI language into Python. Simple enough I hope.

As I understand the Parser has a certain thing it must have before:

**AST**. The parser turns the tokens, which are a flat list, into a tree. That tree should then depict how the program is structured.
For ``x = 1 + 2 * 3;`` our list would just show it in the order it is written: 
```
Assign(x) → Number(1) → Add → Number 2 → Multiply → Number(3)
```
If we ran it that way, the result would be ``9``.
AST makes a tree for us. 
```
Assign(x)
  └─ Add
      ├─ Number(1)
      └─ Multiply
          ├─ Number(2)
          └─ Number(3)
```
That way, the result would be ``7``. Or, well, it should be. 

The overall grammar should then be
```
program     → statement* EOF
statement   → assignment | ifStmt | whileStmt | printStmt
assignment  → IDENTIFIER "=" expression ";"
expression  → comparison
comparison  → term ( ( "<" | ">" | "==" ) term )*
term        → factor ( ( "+" | "-" ) factor )*
factor      → primary ( ( "*" | "/" ) primary )*
primary     → NUMBER | STRING | IDENTIFIER | "(" expression ")"
```

Whilst a parser definitely is hell, building it reminds greatly of EBNF and DFA. So, it
is somewhat fun trying to figure all the checks out. Though debugging errors is quite
exhausting. 

Reminder to anyone doing something like this: Plan debugging asap.

Since Step 1 is done (*parsing expressions*), now it is time to build the program parser. Like, actual functions. Which
should by itself be a harder task than I'd like. However, once the basic build stands stable, building the language around
it should be rather easy. 

The step towards parsing an actual program would be altering our Lexer. 
Simply enough we just have to build a list for keywords. Once again. 

The good think about having ``tokens.py`` is, that anyone could alter how the language is interpreted or what he could write. So, parsing SSI could work in any given language and still work. Though the syntax is similar to JavaScript, one could change keywords for this to be more like Java or more like Python. It's anyones choice. 

But first: Assigning values. ``x = 3`` won't work so far. Which is a somewhat issue. As I understand, I need a ``Scope``-class. Something that remembers, for every function or class, what variables are within that single class. It stores, probably a dict. If a function wants to access a variable it asks the current scope it is in whether it has the variable in his dict. 
If that is so, we stop. Else we search outwards from child to parent.