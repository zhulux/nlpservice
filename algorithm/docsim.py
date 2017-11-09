from . import news_tfidf
import math

def docsim(doc_a, doc_b):
  vec_a = doc_to_vec(doc_a)
  vec_b = doc_to_vec(doc_b)
  return vec_sim(vec_a, vec_b)

def doc_to_vec(doc):
  keyed_vec = dict(news_tfidf(doc))
  norm = math.sqrt(sum([v * v for v in keyed_vec.values()]))
  return { k: v / norm for k, v in keyed_vec.items() }

def vec_sim(vec_a, vec_b):
  intersection = set(vec_a.keys()) & set(vec_b.keys())
  dot_prod = 0.0
  for k in intersection:
    dot_prod += vec_a[k] * vec_b[k]
  return dot_prod

