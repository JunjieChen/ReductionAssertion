import random
import shutil
import os
import copy
import sys
import subprocess as subp
import thread

def exccmd(cmd):
	p=os.popen(cmd,"r")
	rs=[]
	line=""
	while True:
		line=p.readline()
		if not line:
			break
		#print line
		rs.append(line.strip())
	return rs

subjects=['clojure-maven-plugin','glacieruploader','gson-fire']
#'jackson-datatype-joda','IClojure','hashids-java','commons-email','exp4j','redline-smalltalk-master','Confucius','brickhouse'
for s in subjects:
	print s
	exccmd('python randomGenTestSuite-1file.py '+s)
	exccmd('python testCaseReduce-1file.py '+s)

