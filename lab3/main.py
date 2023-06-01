from tokenizer import Tokenizer
from token_parser import Parser


def main():
  with open('./test/test.txt', 'r') as f:
    src_code = f.read().replace('\n', '')

  tokenizer = Tokenizer(src_code)
  tokens = tokenizer.tokenize()
  parser = Parser(tokens)
# try:
  parser.ParseProgram()

  styles = {
    'vertex_size': 5,
    'vertex_label': parser._g.graph.vs['name'],
    'vertex_label_size': 12,
    'vertex_label_dist': 3,
    'bbox': (900, 500),
    'margin': 20,
  }
  parser.display_graph('./res.pdf', 'rt_circular', styles)

  print('\nAccepted')
# except Exception as e:
#   print(e)
#   print('\nRejected')

if __name__ == '__main__':
  main()
