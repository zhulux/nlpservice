import traceback

def render_json(func):
  def func_wrapper(*args, **kwargs):
    try:
      result = func(*args, **kwargs)
      return {
        'status': 'ok',
        'result': result
      }
    except Exception as e:
      return {
        'status': 'error',
        'error': str(e),
        'details': traceback.format_exc().split('\n')
      }

  return func_wrapper
