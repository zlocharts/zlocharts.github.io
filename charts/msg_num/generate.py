#!/usr/bin/env python
from os import path
from sys import argv
import sqlite3

print 'Regenerating msg_num...'

db_name = path.dirname(argv[0]) + '/../../board.db'
conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
cur = conn.cursor()

cur.execute('SELECT date, id FROM messages WHERE id % 10000 = 0')
f = file(path.dirname(argv[0]) + '/msg.csv', 'w')
f.write('date,id\n')
for r in cur:
  f.write(str(r[0]) + ',' + str(r[1]) + '\n')
f.close()

print 'Done'

# Gather information about million gets and predict the date of the next one.
cur.execute('SELECT max(id) FROM messages')
max_id = cur.fetchone()[0]
cur.close

def GetOrGuessDate(msg_num):
  global cur
  cur.execute('SELECT date FROM messages WHERE id == ?', (msg_num,))
  res = cur.fetchone()
  if res is not None:
    return res[0]
  # Message is not available, guess the date as a median from neighbours.
  d_before, d_after = None, None
  i = msg_num
  while d_before is None and i > 0:
    i -= 1
    cur.execute('SELECT date FROM messages WHERE id == ?', (i,))
    res = cur.fetchone()
    if res is not None:
      d_before = res[0]
  global max_id
  i = msg_num
  while d_after is None and i < max_id:
    i += 1
    cur.execute('SELECT date FROM messages WHERE id == ?', (i,))
    res = cur.fetchone()
    if res is not None:
      d_after = res[0]
  if d_before is None or d_after is None:
    return d_before or d_after
  return d_before + (d_after - d_before) / 2

i = 1000000
while i < max_id:
  print i, GetOrGuessDate(i)
  i += 1000000

import datetime
month_ago = datetime.datetime.now() - datetime.timedelta(30)
x, y = [], []
cur.execute('SELECT date, id FROM messages WHERE date > ?', (month_ago,))
for r in cur:
  x.append(r[1])
  y.append(int(r[0].strftime('%s')))

from scipy.stats import linregress

# y = kx + b
k, b, _, _, _ = linregress(x, y)

# Next get
next_sec = k * i + b
d_next = datetime.datetime.fromtimestamp(next_sec)
print i, 'ETA:', d_next
