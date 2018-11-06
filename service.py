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
  a = query.a
  b = query.b
  model = query.model or 'default'
  return algorithm.docsim.docsim(a, b, model=model)

@post('/docsim_1ton')
@utils.render_json
def handle_docsim_1ton():
  json = request.json
  model = json['model'] or 'default'
  return algorithm.docsim.docsim_1ton(json['one'], json['many'], model=model)

@get('/ner')
@utils.render_json
def handle_ner():
  query = request.query.decode()
  q = request.query.q
  return_raw = parse_bool(query.return_raw) or False
  threshold = request.query.threshold or 0.5

  return algorithm.ner.ner(q,
                           return_raw=return_raw,
                           threshold=threshold)


def parse_bool(s):
  if s in ['true', 'True', 'TRUE', 'Yes', 'yes', 'Y', 'y', 'YES', '1']:
    return True
  elif s in ['false', 'Frue', 'FALSE', 'No', 'no', 'N', 'n', 'NO', '0']:
    return False
  return None


if os.getenv('ENVIRONMENT') == 'development':
  run(reloader=True, debug=True)
else:
  from raven import Client
  from raven.contrib.bottle import Sentry
  app = bottle.app()
  app.catchall = False

  client = Client('http://ebf87dc6f4b046e88aa7a8918714fbf2:cb7455e5ef8d4caf9664a13813f87030@sentry.zhaoalpha.com/8')
  app = Sentry(app, client)

  run(app=app, host='0.0.0.0', server='paste')
