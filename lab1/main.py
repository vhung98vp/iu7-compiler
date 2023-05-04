from regex import GrammarToRegex
from nfa import RegexToNFA
from dfa import NFAToDFA


def main():
  with open('test/test_grammar.txt') as f:
    grammars = f.read().strip().split('\n\n')
    for grammar in grammars:
      grm = GrammarToRegex(grammar)
      print("\n1) System of equations:")
      print(grm.getEquations())

      regexSystem = grm.getRegexSystem()
      print("\n2) System of regex:")
      print(regexSystem)

      regex = list(regexSystem.values())[0]
      nfa = RegexToNFA(regex).getNFA()
      print("\nFirst regex:", regex)
      print("3) NFA of first regex: ")
      nfa.display()

      dfa = NFAToDFA(nfa).getDFA()
      print("\n4) DFA of first regex: ")
      dfa.display()

      nfa.drawGraph("nfa")
      dfa.drawGraph("dfa")

if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print("\nFailure:", e)