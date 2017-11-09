import jieba
import jieba.analyse

jieba.initialize()
jieba.load_userdict('models/dicts/stocks.txt')
jieba.load_userdict('models/dicts/finance_terms.txt')

def news_tfidf(sent):
  if not hasattr(news_tfidf, 'model'):
    news_tfidf.model = jieba.analyse.TFIDF(idf_path='models/dicts/news_idf.txt')
  return news_tfidf.model.extract_tags(sent, withWeight=True)


