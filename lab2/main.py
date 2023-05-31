from utils import eliminate_left_recursion, remove_inaccessible

def main():
  fi1 = './test/test1.txt'
  fo1 = './test/res1.txt'

  elr = eliminate_left_recursion(fi1)
  elr.export_to_file(fo1)

  fi2 = './test/test2.txt'
  fo2 = './test/res2.txt'
  ri = remove_inaccessible(fi2)
  ri.export_to_file(fo2)

if __name__ == '__main__':
  try:
    main()
  except BaseException as e:
    print("\nFailure:", e)