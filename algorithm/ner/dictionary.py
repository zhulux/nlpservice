import json
import os
import numpy as np

VOCAB_MODEL_FILE = 'vocab-20181105.db'

class Dictionary:
  def __init__(self):
    # 0 reserved for padding char
    # 1 reserved for unknown char
    self.num_chars = 2
    self.dict = {}

  def add_string(self, string):
    for c in string:
      self.add_char(c)

  def add_char(self, c):
    if c not in self.dict:
      self.dict[c] = self.num_chars
      self.num_chars += 1

  def find_char(self, c):
    if c in self.dict:
      return self.dict[c]
    else:
      return 1

  def write_metadata(self, filename='metadata.tsv'):
    rest = [name for idx,name in sorted((idx,name) for name,idx in self.dict.items())]
    with open(filename, 'w') as f:
      f.write('PAD\n')
      f.write('UNK\n')
      for s in rest:
        f.write(repr(s)[1:-1])
        f.write('\n')

  # output shape: (len(ss))
  def prepare_input_sequence(self, s, seq_len=None):
    if seq_len is None:
      return np.array([self.find_char(c) for c in s])
    else:
      t = np.zeros([seq_len], dtype='long')
      t[:len(s)] = np.array([self.find_char(c) for c in s])[:seq_len]
      return t

  # output shape: (seq_len)
  def prepare_tag_sequence(self, seq_len, entity_beg, entity_len):
    t = np.zeros(seq_len)
    t[entity_beg:entity_beg+entity_len] = 1.0
    return t

  # output type: (in, targ), in.size() = targ.size() = (len(s))
  def prepare_example(self, s, entity_beg, entity_len):
    inputs = self.prepare_input_sequence(s)
    targets = self.prepare_tag_sequence(len(s), entity_beg, entity_len)
    return inputs, targets

  # input type:  array of [title, entity_beg, entity_len]
  # output type: (in, targ), in.size() = targ.size() = (len(records), max(len(records[0])))
  def prepare_examples(self, records, fixlen=None):
    seq_len = None
    if fixlen is None:
      seq_len = max(len(r[0]) for r in records)
    else:
      seq_len = fixlen

    batch_size = len(records)
    input_tensor = np.zeros([batch_size, seq_len], dtype='long')
    target_tensor = np.zeros([batch_size, seq_len], dtype='float32')
    for i,r in enumerate(records):
      input_tensor[i, :] = self.prepare_input_sequence(r[0], seq_len)
      target_tensor[i, :] = self.prepare_tag_sequence(seq_len, r[1], r[2])
      # return input_tensor, target_tensor.reshape(batch_size, max_seq_len, 1)
    return input_tensor, target_tensor


  def save(self, file):
    with open(file, 'w') as f:
      json.dump({ 'n': self.num_chars, 'd': self.dict }, f)
  def load(self, file):
    with open(file) as f:
      obj = json.load(f)
      self.num_chars = obj['n']
      self.dict = obj['d']

vocab = Dictionary()
vocab.load(f'models/ner/{VOCAB_MODEL_FILE}')
