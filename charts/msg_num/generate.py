#!/usr/bin/env python
from os import path
from sys import argv
import sqlite3

print 'Regenerating msg_num...'

db_name = path.dirname(argv[0]) + '/../../board.db'
conn = sqlite3.connect(db_name)
cur = conn.cursor()

cur.execute('SELECT date, id FROM messages WHERE id % 10000 = 0 ORDER BY date')
f = file(path.dirname(argv[0]) + '/msg.csv', 'w')
f.write('date,id\n')
for r in cur:
  f.write(str(r[0]) + ',' + str(r[1]) + '\n')
f.close()

print 'Done'
