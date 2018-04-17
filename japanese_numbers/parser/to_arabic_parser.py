#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

from japanese_numbers.token import Tokenized, NUMERICS
from japanese_numbers.kind import (  # noqa
  UNIT_KIND,
  NUMBERS_KIND,
  MULTIPLES_KIND,
  NUMERIC_KIND
)


def _collect_numerics(val, pos):
  stack = []
  for c in val[pos:]:
    if c not in NUMERICS:
      break
    stack.append(c)
  return int(''.join(stack)), len(stack)


def to_arabic(val, encode='utf8'):  
  stacks, numbers, texts, analyzing, index = ([], [], [], False, -1)
  results = []

  # function for collecting results
  def _append_result():
    results.append(sum(stacks) + sum(numbers))

  # make sure the value is unicode
  decoded_val = val if isinstance(val, str) else val.decode(encode)
  token = Tokenized(decoded_val)

  # iterate over value
  while token.has_next():
    kind, num = (token.kind, token.num_of_kind)
    
    if kind == UNIT_KIND and token.last_kind != UNIT_KIND:
      ret = (numbers[-1] if numbers else 1) * num
      if numbers:
        numbers[-1] = ret
      else:
        numbers.append(ret)

    elif kind in (NUMBERS_KIND, UNIT_KIND):
      numbers.append(num)

    elif kind == MULTIPLES_KIND:
      stacks.append(sum(numbers) * num)
      numbers = []

    elif kind == NUMERIC_KIND:
      n, s = _collect_numerics(token.val, token.pos)
      numbers.append(n)
      index = token.pos if index < 0 else index
      texts.append(''.join(token.origin_char_at(x)
                   for x in range(token.pos, token.pos + s)))
      token.next(incr=s)

    elif analyzing:

      _append_result()
      stacks, numbers, texts, analyzing, index = ([], [], [], False, -1)
      
    analyzing = kind is not None

    if analyzing:
      if kind != NUMERIC_KIND:
        texts.append(token.origin_char)
      if index < 0 and token.last_kind is None:  # 1st time:
        index = token.pos

    if kind != NUMERIC_KIND:
      token.next()

  if stacks or numbers:
    _append_result()
  
  return results


def to_arabic_numbers(val, encode='utf8'):
  return tuple(x.number for x in to_arabic(val, encode=encode))



def demo():
  nums= to_arabic('銀河の向こう、六千三百二十一億千五百十一万二千百八十一光年彼方。')
  print(nums)
    
  
if __name__ == "__main__":
  demo()
