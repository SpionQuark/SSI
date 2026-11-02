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
