import logging
import utils
import algorithm
import bottle
import os
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

if os.getenv('environment') == 'development':
  run(reloader=True, debug=True)
else:
  from raven import Client
  from raven.contrib.bottle import Sentry
  app = bottle.app()
  app.catchall = False

  client = Client('http://ebf87dc6f4b046e88aa7a8918714fbf2:cb7455e5ef8d4caf9664a13813f87030@sentry.zhaoalpha.com/8')
  app = Sentry(app, client)

  run(app=app, host='0.0.0.0', server='paste')

