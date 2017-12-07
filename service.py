import logging
import utils
import algorithm
import bottle
from bottle import get, post, route, run, request

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 # 1MB max req size

@get('/docsim')
@utils.render_json
def handle_docsim():
  query = request.query.decode()
  a = query.a or ''
  b = query.b or ''
  model = query.model or 'default'
  return algorithm.docsim.docsim(a, b, model=model)

@post('/docsim_1ton')
@utils.render_json
def handle_docsim_1ton():
  json = request.json
  model = json['model']
  return algorithm.docsim.docsim_1ton(json['one'], json['many'], model=model)

run(reloader=True)
