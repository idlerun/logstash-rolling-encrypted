#!/usr/bin/python

import sys, os
import argparse

import logging
import time 
from logging.handlers import RotatingFileHandler

parser = argparse.ArgumentParser(description='Read from stdin and log to a rolling file')
parser.add_argument('--out', help='log file to write output to (with file rolling)', required=True)
args = parser.parse_args()

logger = logging.getLogger("_")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(args.out, maxBytes=10000000, backupCount=10)
handler.setFormatter(logging.Formatter(fmt='%(message)s'))
logger.addHandler(handler)
	
for line in sys.stdin:
	line = line.replace('\r', '').replace('\n', '')
	logger.info(line)
