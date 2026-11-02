# Lexer Build docs

So, from what I get so far, a lexer is used to turn code into the smallest bits possible. Like
```python
x = 3 + 42
```
would turn into something like
```python
IDENTIFIER(x) EQUALS NUMBER(3) PLUS NUMBER(42)
```

It also removes whitespace and comments. So, it sort of cleans the code for the parser to run on it. 

Simplest approach for that is just building a loop with several ``if`` states. It iterates over the characters and tries to extract all tokens.

Adding the functions ``read_number()`` and ``read_word()`` help reading even the numbers. The test string ``if x > 0:\n    return x`` however could not be read succesfully, because I forgot that operators should be tokenized as well. So, ``>`` I forgot, therefor it raises an exception.

Also, because testing the lexer can be annoying, there now is a test-suite in ``lexer_test.py``. You can just add further functions. 

Whilst testing the evaluator an issue surfaced:
    **What if there is no spacing?**
From writing code I know that laziness kicks in after few hours of working on the hardest bugs.
So, instead of writing the clean ``1 + 1``, you just put ``1+1`` right there. But, the lexer kinda
needs you to use spacings, else it gets sort of a stroke. So, to prevent that from happening, all 
no-spacing-cases must also be worked on. This can either done by using a seperator-check or by using
the word book and just add all edge cases (like ``-(`` or ``)*-(``). Since there can probably be infinite
posibilities on how to get edge cases when using no spacing, the better solution is to build a rigid check.