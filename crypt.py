#!/usr/bin/python

import sys, os, math
import argparse
from Crypto.Cipher import AES
from bitstring import BitStream

parser = argparse.ArgumentParser(description='Read from stdin and encrypt each line with AES key (to hex encoding)')
parser.add_argument('--key', help='file containing the AES encryption key', required=True)
args = parser.parse_args()

with open (args.key, "rb") as f:
	key = f.read()
	
for line in sys.stdin:
	# 16 byte random iv per line
	iv = BitStream(os.urandom(16))
	line = line.replace('\r', '').replace('\n', '')
	padToLen = max(16, math.ceil(len(line) / 16) * 16)
	cryptIn = line + '\x00' * (padToLen - len(line))
	crypter = AES.new(key, AES.MODE_CBC, iv.bytes)
	result = BitStream(crypter.encrypt(cryptIn))
	output = iv + result
	# first 32 hex digits of every line is the IV
	sys.stdout.write(output.hex + "\r\n")
	sys.stdout.flush()
