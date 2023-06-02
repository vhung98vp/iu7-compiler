import io
from token_type import *


class Tokenizer:
  def __init__(self, text):
    self._text = text
    self._reader = io.StringIO(text)

  def peek(self):
    ch = self._reader.read(1)
    if ch:
      self._reader.seek(self._reader.tell() - 1)
    return ch

  def tokenize(self):
    tokens = []

    while self.peek():
      while self.peek().isspace():
        self._reader.read(1)
      if not self.peek():
        break

      if self.peek().isdigit():
        num = self.parse_number()
        tokens.append(NumberToken(num))

      c = self.peek()
      if c == '(':
        tokens.append(OpenParenthesisToken())
        self._reader.read(1)
      elif c == ')':
        tokens.append(CloseParenthesisToken())
        self._reader.read(1)
      elif c == '<':
        tokens.append(LessToken())
        self._reader.read(1)
        c = self.peek()
        if (c == '='):
          tokens.pop()
          tokens.append(LessEqualToken())
          self._reader.read(1)
        elif (c == '>'):
          tokens.pop()
          tokens.append(NotEqualToken())
          self._reader.read(1)
      elif c == '>':
        tokens.append(GreaterToken())
        self._reader.read(1)
        c = self.peek()
        if (c == '='):
          tokens.pop()
          tokens.append(GreaterEqualToken())
          self._reader.read(1)
      elif c == '=':
        tokens.append(AssignmentToken())
        self._reader.read(1)
        c = self.peek()
        if (c == '='):
          tokens.pop()
          tokens.append(EqualToken())
          self._reader.read(1)
      elif c == '+':
        if isinstance(tokens[-1], AssignmentToken) or isinstance(tokens[-1], RelationToken):
          tokens.append(PositiveToken())
        else:
          tokens.append(PlusToken())
        self._reader.read(1)
      elif c == '-':
        if isinstance(tokens[-1], AssignmentToken) or isinstance(tokens[-1], RelationToken):
          tokens.append(NegativeToken())
        else:
          tokens.append(MinusToken())
        self._reader.read(1)
      elif c == '*':
        tokens.append(MultiplyToken())
        self._reader.read(1)
      elif c == '/':
        tokens.append(DivideToken())
        self._reader.read(1)
      elif c == '{':
        tokens.append(OpenCurlyBracketToken())
        self._reader.read(1)
      elif c == '}':
        tokens.append(CloseCurlyBracketToken())
        self._reader.read(1)
      elif c == ';':
        tokens.append(SemicolonToken())
        self._reader.read(1)
      else:
        while self.peek().isspace():
          self._reader.read(1)
        if not self.peek():
          break
        if c.isalpha():
          id = self.parse_identifier()
          tokens.append(self.parse_keyword(id))

    return tokens

  def parse_number(self):
    digits = str()
    while self.peek().isdigit():
      digits += self._reader.read(1)
    return int(digits)

  def parse_identifier(self):
    id = str()
    while self.peek().isalpha() or self.peek() == '_':
      id += self._reader.read(1)    
    return id
  
  def parse_keyword(self, id):
    if id == 'and':
      return AndToken()
    elif id == 'or':
      return OrToken()
    elif id == 'not':
      return NotToken()
    elif id == 'div':
      return DivisionToken()
    elif id == 'mod':
      return ModulusToken()
    else:
      return IdentifierToken(id)