from aiohttp import web
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


app = web.Application()
app.router.add_routes(routes)

web.run_app(app)


