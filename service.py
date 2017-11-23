from aiohttp import web
import logging
import utils
import algorithm

routes = web.RouteTableDef()

@routes.get('/docsim')
@utils.render_json
async def handle_docsim(req):
  a = req.query.get('a', '')
  b = req.query.get('b', '')
  model = req.query.get('model', 'default')
  return algorithm.docsim.docsim(a, b, model=model)

@routes.post('/docsim_1ton')
@utils.render_json
async def handle_docsim_1ton(req):
  json = await req.json()
  model = json['model']
  return algorithm.docsim.docsim_1ton(json['one'], json['many'], model=model)

app = web.Application()
app.router.add_routes(routes)

logger = logging.getLogger("NLP")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
app.make_handler(access_log=logger)

web.run_app(app, port=8080, access_log=logger)
