import traceback

def render_json(func):
  def func_wrapper(*args, **kwargs):
    result = func(*args, **kwargs)
    return {
      'status': 'ok',
      'result': result
    }
  return func_wrapper
