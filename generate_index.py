#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
template = env.get_template('index.tmpl.html')
content = template.render()

f = open('index.html', 'w')
f.write(content.encode('utf-8'))
f.close()
