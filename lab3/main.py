from tokenizer import Tokenizer
from token_parser import Parser


def main():
  with open('./test/test.txt', 'r') as f:
    src_code = f.read().replace('\n', '')

  tokenizer = Tokenizer(src_code)
  tokens = tokenizer.tokenize()
  parser = Parser(tokens)
  try:
    parser.ParseProgram()
    parser.display_graph('./res.png')
    print('\nAccepted')
  except Exception as e:
    print(e)
    print('\nRejected')

if __name__ == '__main__':
  main()
