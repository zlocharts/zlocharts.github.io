#!/usr/bin/env python

import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('../../board.db')
cur = conn.cursor()

# Top 200 users by messages num for the last week.
week_ago = datetime.now() - timedelta(8)
cur.execute('SELECT nick, count(*) as num '
            'FROM messages WHERE date > ? '
            'GROUP BY nick ORDER BY num DESC LIMIT 100', (week_ago,))

children = []
for r in cur:
    children.append({'name': r[0], 'size': r[1]})

result = {'name': 'board.rt.mipt.ru', 'children': children}

import json

# Write to top200.json
f = open('top200.json', 'w')
json.dump(result, f)
f.close()
