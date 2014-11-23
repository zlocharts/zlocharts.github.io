#!/bin/bash

DIRNAME=`dirname $0`

$DIRNAME/update_db.py || exit 1
$DIRNAME/charts/bubbles_top/generate.py
$DIRNAME/charts/msg_num/generate.py
