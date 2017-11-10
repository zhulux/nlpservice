from . import tfidf
import math

def docsim(doc_a, doc_b, model='default'):
  vec_a = doc_to_vec(doc_a, model)
  vec_b = doc_to_vec(doc_b, model)
  return vec_sim(vec_a, vec_b)

def doc_to_vec(doc, model):
  keyed_vec = dict(tfidf(doc, model))
  norm = math.sqrt(sum([v * v for v in keyed_vec.values()]))
  return { k: v / norm for k, v in keyed_vec.items() }

def vec_sim(a, b):
  intersection = set(a.keys()) & set(b.keys())
  return sum([a[k] * b[k] for k in intersection])

