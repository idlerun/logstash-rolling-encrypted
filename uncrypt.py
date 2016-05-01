#!/usr/bin/python

import sys
import argparse
from Crypto.Cipher import AES
from bitstring import BitStream

parser = argparse.ArgumentParser(description='Read from stdin and decrypt each line with AES key (from hex encoding)')
parser.add_argument('--key', help='file containing the AES encryption key', required=True)
args = parser.parse_args()

with open (args.key, "rb") as f:
	key = f.read()

for line in sys.stdin:
	line = line.replace('\r','').replace('\n', '')
	if len(line) == 0:
		continue
	try:
		line = BitStream(hex=line)
		iv = line[0:128]
		data = line[128:]
		#print("iv=%s, data=%s" % (iv.hex, data.hex))
		crypter = AES.new(key, AES.MODE_CBC, iv.bytes)
		output = crypter.decrypt(data.bytes).decode('ascii').replace('\00', '')
		sys.stdout.write(output + "\r\n")
		sys.stdout.flush()
	except ValueError as e:
		print("ValueError: %s" % e, file=sys.stderr)
	except:
		print("ERROR %s, LINE=%s" % (sys.exc_info()[0], line), file=sys.stderr)
