from . import tfidf
import math
from functools import lru_cache

class NamedVec(dict):
  def __hash__(self):
    return hash(frozenset(self.items()))

def docsim(doc_a, doc_b, model='default'):
  vec_a = doc_to_vec(doc_a, model)
  vec_b = doc_to_vec(doc_b, model)
  return vec_sim(vec_a, vec_b)

def docsim_1ton(one, many, model='default'):
  vec_one = doc_to_vec(one, model)
  vec_many = [doc_to_vec(x, model) for x in many]
  return [vec_sim(vec_one, x) for x in vec_many]

@lru_cache(maxsize=1024)
def doc_to_vec(doc, model):
  keyed_vec = dict(tfidf(doc, model))
  norm = math.sqrt(sum([v * v for v in keyed_vec.values()]))
  return NamedVec({ k: v / norm for k, v in keyed_vec.items() })

@lru_cache(maxsize=1024)
def vec_sim(a, b):
  intersection = set(a.keys()) & set(b.keys())
  return sum([a[k] * b[k] for k in intersection])
