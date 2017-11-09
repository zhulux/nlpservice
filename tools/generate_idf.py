#
# Usage: python $0 corpus_file
#
#

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

import math
import algorithm

jieba = algorithm.jieba

def main():
  vocab = {}
  count = 0
  with open(sys.argv[1]) as f:
    for line in f:
      line = line.strip()
      count += 1
      for word in set(jieba.lcut(line, cut_all=True)):
        if len(word.strip()) == 0:
          continue
        vocab[word] = vocab.get(word, 0) + 1

  for term, freq in vocab.items():
    idf = math.log(count / (1 + freq))
    print(f"{term} {idf}")
  

if "__main__" == __name__:
  main()

