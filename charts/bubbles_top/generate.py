#!/usr/bin/env python

import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('../../board.db')
cur = conn.cursor()

# Top 100 users by messages num for the last week.
week_ago = datetime.now() - timedelta(8)
cur.execute('SELECT nick, count(*) as num '
            'FROM messages WHERE date > ? '
            'GROUP BY nick ORDER BY num DESC LIMIT 100', (week_ago,))

SPLIT_NUM = 1
children = []
children_split = []
total_num = 0
for r in cur:
    total_num += 1
    children_split.append({'name': r[0], 'size': r[1]})
    if len(children_split) == SPLIT_NUM:
        children.append({'name': 'top' + str(total_num),
                         'children': children_split})
        children_split = []

result = {'name': 'board.rt.mipt.ru', 'children': children}

import json

# Write to top100.json
f = open('top100.json', 'w')
json.dump(result, f)
f.close()
