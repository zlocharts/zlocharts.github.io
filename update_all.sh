#!/bin/bash

DIRNAME=`dirname $0`

$DIRNAME/update.py
$DIRNAME/charts/bubbles_top/generate.py
$DIRNAME/charts/msg_num/generate.py
