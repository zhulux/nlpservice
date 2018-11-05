import traceback
import sys

def render_json(func):
  def func_wrapper(*args, **kwargs):
    try:
      result = func(*args, **kwargs)
      return {
        'status': 'ok',
        'result': result
      }
    except:
      raise
      return {
        'status': 'error',
        'error': [str(e) for e in sys.exc_info()[:-1]]
      }

  return func_wrapper
