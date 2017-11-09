from aiohttp import web

def render_json(func):
  async def func_wrapper(req):
    try:
      result = await func(req)
      return web.json_response({
        'status': 'ok',
        'result': result
      })
    except Exception as e:
      return web.json_response({
        'status': 'error',
        'error': str(e)
      })
      
  return func_wrapper

