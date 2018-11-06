import numpy as np
from itertools import groupby

from .dictionary import vocab
from .nn import model


def ner(sentence, return_raw=False, threshold=0.5):
  inputs = vocab.prepare_input_sequence(sentence).reshape(1, -1)
  outputs = model.predict(inputs).reshape(-1)
  pos_conf, oa_conf = confidence(outputs, threshold)
  error = None
  raw = list(zip(sentence, outputs.tolist()))

  entity_name = extract_word(sentence, outputs, threshold)
  result = {
    'threshold': threshold,
    'positive_confidence': pos_conf,
    'overall_confidence': oa_conf,
    'entity': entity_name
  }

  if return_raw:
    result['raw'] = raw

  return result



def extract_word(sentence, outputs, threshold):
  group = valid_group(outputs, threshold)
  if group is None:
    return None
  w = [sentence[i] for i in group]
  return ''.join(w)

def valid_group(outputs, threshold):
  outputs = enumerate(outputs)
  above_threshold = lambda x: x[1] >= threshold
  groups = [(pos, list(v)) for pos, v in groupby(outputs, key=above_threshold)]
  pos_group_count = len(list(1 for pos,_ in groups if pos))

  if pos_group_count != 1:
    return None

  for pos, val in groups:
    if pos:
      return [i for i,_ in val]

  return None

def confidence(outputs, threshold):
  goals = np.copy(outputs)
  goals[outputs >= threshold] = 1.0
  goals[outputs <  threshold] = 0.0

  def stddev(ary):
    if ary is None or len(ary) == 0:
      return 0.0
    return 1 - 2 * np.sqrt(np.mean(np.square(ary)))

  diff = outputs - goals

  positive = stddev(diff[outputs >= threshold])
  overall = stddev(diff)

  return positive, overall
