#!/usr/bin/env python

import sys
import re

def ip2int(ip) :
	ret = 0
	match = re.match("(\d*)\.(\d*)\.(\d*)\.(\d*)", ip)
	if not match : return 0
	for i in xrange(4) : ret = (ret << 8) + int(match.groups()[i])
	return ret

def int2ip(ipnum) :
	ip1 = ipnum >> 24
	ip2 = ipnum >> 16 & 0xFF
	ip3 = ipnum >> 8 & 0xFF
	ip4 = ipnum & 0xFF
	return "%d.%d.%d.%d" % (ip1, ip2, ip3, ip4)

def getrange(startip, endip) :
	result = []
	bits = 1
	mask = 1
	while bits < 32 :
		newip = startip | mask
		if (newip>endip) or (((startip>>bits) << bits) != startip) :
			bits = bits - 1
			mask = mask >> 1
			break
		bits = bits + 1
		mask = (mask<<1) + 1
	newip = startip | mask
	bits = 32 - bits
	result.append( "%s/%d" % (int2ip(startip), bits) )
	if newip < endip : 
		result.extend( getrange(newip + 1, endip) )
	return result
