from aiohttp import web
import utils
import algorithm

routes = web.RouteTableDef()

@routes.get('/jieba/cut')
@utils.render_json
async def handle_jieba_cut(req):
  sent = req.query.get('sentence', 'hello world')
  return algorithm.jieba.lcut(sent)

@routes.get('/jieba/tfidf')
@utils.render_json
async def handle_jieba_tfidf(req):
  sent = req.query.get('sentence', 'hello world')
  return algorithm.jieba.analyse.extract_tags(sent, withWeight=True)


app = web.Application()
app.router.add_routes(routes)

web.run_app(app)


