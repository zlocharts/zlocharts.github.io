#!/usr/bin/env python
"""
Create board.db if doesn't exist, update it otherwise.
"""

import datetime
import sqlite3
import sys
from suds import WebFault
from suds.client import Client

ZLO_ID = 0
DB_NAME = 'board.db'

SPEED_UPDATE_INT = 10

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# Create table
cur.execute('CREATE TABLE IF NOT EXISTS messages (body text, date timestamp,'
            'hasImg boolean, hasUrl boolean, host text, id integer PRIMARY KEY,'
            'nick text, reg boolean, title text, topic text)')
# And index
cur.execute('CREATE INDEX IF NOT EXISTS DateIndex ON messages (date);')

c = Client('http://zlo.rt.mipt.ru:7500/ws/search?wsdl')
service = c.service

cur.execute('SELECT MAX(id) FROM messages')
max_result = cur.fetchone()

last_saved = 0 if max_result is None else max_result[0]
last_indexed = service.getLastSavedMsgNumber(ZLO_ID)

start_time = datetime.datetime.now()
msg_per_sec = 0.0

added_num = 0
failed_num = 0
try:
  for x in xrange(last_saved + 1, last_indexed + 1):
    # Try again on fault.
    msg = {}
    fail_num = 0
    while True:
      try:
        msg = service.getMessage(ZLO_ID, x)
        break
      except WebFault as wb:
        fail_num += 1
        if fail_num > 3:
          print '\rWebFault (#%d):' % x, wb.message
          failed_num += 1
          break
        continue
      except Exception as e:
        print '\rCannot parse message #%d:' % x, e.message
        break
    try:
      cur.execute('INSERT INTO messages VALUES (?,?,?,?,?,?,?,?,?,?)',
                  (msg.body, msg.date, msg.hasImg, msg.hasUrl, msg.host,
                   msg.id, msg.nick, msg.reg, msg.title, msg.topic))
      added_num += 1
    except AttributeError:
      # Message doesn't exist
      failed_num += 1
    if x % SPEED_UPDATE_INT == 0:
      current_time = datetime.datetime.now()
      delta = current_time - start_time
      if delta.total_seconds() != 0:
        msg_per_sec = (x - last_saved) / delta.total_seconds()
    eta_sec = int((last_indexed - x) /
                  (msg_per_sec if msg_per_sec != 0 else 0.01))
    print ('\r[%d/%d] Loading messages... (%.2f msg/sec, %.2d:%.2d:%.2d ETA)' %
           (x, last_indexed, msg_per_sec, eta_sec / 3600,
            (eta_sec % 3600) / 60, eta_sec % 60)),
    sys.stdout.flush()
    if x % 1000 == 0:
      conn.commit()
finally:
  conn.commit()
  conn.close()
  print ('\nTotal added: %d\nTotal failed: %d (Err %.2f%%)' %
         (added_num, failed_num, float(failed_num) /
          (added_num if added_num != 0 else 1) * 100))
