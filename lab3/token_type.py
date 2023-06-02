class Token: pass

class ParenthesisToken(Token): pass
class OpenParenthesisToken(ParenthesisToken):
  def __init__(self):
    self.val = '('
class CloseParenthesisToken(ParenthesisToken):
  def __init__(self):
    self.val = ')'

class CurlyBracket(Token): pass
class OpenCurlyBracketToken(CurlyBracket):
  def __init__(self):
    self.val = '{'
class CloseCurlyBracketToken(CurlyBracket):
  def __init__(self):
    self.val = '}'

class RelationToken(Token): pass
class LessToken(RelationToken):
  def __init__(self):
    self.val = '<'
class LessEqualToken(RelationToken):
  def __init__(self):
    self.val = '<='
class GreaterToken(RelationToken):
  def __init__(self):
    self.val = '>'
class GreaterEqualToken(RelationToken):
  def __init__(self):
    self.val = '>='
class EqualToken(RelationToken):
  def __init__(self):
    self.val = '=='
class NotEqualToken(RelationToken):
  def __init__(self):
    self.val = '<>'

class AdditionToken(Token): pass
class PlusToken(AdditionToken):
  def __init__(self):
    self.val = '+'
class MinusToken(AdditionToken):
  def __init__(self):
    self.val = '-'
class OrToken(AdditionToken):
  def __init__(self):
    self.val = 'or'

class SignToken(Token): pass
class PositiveToken(SignToken):
  def __init__(self):
    self.val = '+'
class NegativeToken(SignToken):
  def __init__(self):
    self.val = '-'

class MultiplicationToken(Token): pass
class MultiplyToken(MultiplicationToken):
  def __init__(self):
    self.val = '*'
class DivideToken(MultiplicationToken):
  def __init__(self):
    self.val = '/'
class DivisionToken(MultiplicationToken):
  def __init__(self):
    self.val = 'div'
class ModulusToken(MultiplicationToken):
  def __init__(self):
    self.val = 'mod'
class AndToken(MultiplicationToken):
  def __init__(self):
    self.val = 'and'

class NotToken(Token):
  def __init__(self):
    self.val = 'not'

class AssignmentToken(Token):
  def __init__(self):
    self.val = '='
class SemicolonToken(Token):
  def __init__(self):
    self.val = ';'

class NumberToken(Token):
  def __init__(self, val):
    self.val = val

class IdentifierToken(Token):
  def __init__(self, val):
    self.val = val

class ErrorToken(Token): pass