#!/usr/bin/env python
import sqlite3

print 'Regenerating msg_num...'

conn = sqlite3.connect('../../board.db')
cur = conn.cursor()

cur.execute('SELECT date, id FROM messages WHERE id % 10000 = 0 ORDER BY date')
f = file('msg.csv', 'w')
f.write('date,id\n')
for r in cur:
  f.write(str(r[0]) + ',' + str(r[1]) + '\n')
f.close()

print 'Done'
