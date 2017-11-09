import jieba
import jieba.analyse

jieba.initialize()
jieba.load_userdict('models/dicts/stocks.txt')
jieba.load_userdict('models/dicts/finance_terms.txt')

def tfidf(sent, model='default'):
  if not hasattr(tfidf, 'models'):
    tfidf.models = {}

  if model not in tfidf.models:
    if model in ['news']:
      tfidf.models[model] = jieba.analyse.TFIDF(idf_path=f'models/dicts/{model}_idf.txt')
    else:
      print(f"Warn: loading unknown model [{model}]")
      tfidf.models[model] = jieba.analyse.TFIDF()

  return tfidf.models[model].extract_tags(sent, withWeight=True)


from . import docsim


