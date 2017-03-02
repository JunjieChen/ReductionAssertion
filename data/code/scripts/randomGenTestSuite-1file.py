import random
import shutil
import os
import copy
import sys
import subprocess as subp
import thread

subject = sys.argv[1]
os.chdir('../' + subject)
repeatTimes = 1000

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

filemethod = open('./coverageFiles/' + 'IndexAll.txt','w')

with open('./coverageFiles/index.txt') as infile:
	testSuite = []
	for line in infile:
		testSuite.append(line.strip())
		filemethod.write(line.strip()+'\n')

filemethod.close()

coverages = ['branch', 'method', 'statement', 'mutation']
#reductionApproachs = ['Greedy', 'GE', 'GRE', 'HGS', 'ILP']
#prioritizationApproach = ['ArtMaxMin', 'GreedyTotal', 'GreedyAdditional', 'Genetic']
newfileindexPath = './coverageFiles/randomGen'
if os.path.exists(newfileindexPath):
	exccmd('rm -rf ' + newfileindexPath)
exccmd('mkdir ' + newfileindexPath)

for cnt in range(repeatTimes):
	candidatePool = [i for i in range(len(testSuite))]
	random.shuffle(candidatePool)
	rnd = random.randint(2, len(testSuite))

	randomTestSuite = []
	for tmp in range(rnd):
		randomTestSuite.append(testSuite[candidatePool[tmp]])

	#update index, binary
	for cov in coverages:
		fileindex = open('./coverageFiles/' + 'index.txt')
		lineindex = fileindex.readlines()
		fileindex.close()

		filebinary = open('./coverageFiles/' + cov + 'CoverageBinary.txt')
		linebinary = filebinary.readlines()
		filebinary.close()

		newfileindex = file(newfileindexPath + '/' + cov + 'Index.txt','a+')
		newfilebinary = file(newfileindexPath + '/' + cov + 'CoverageBinary.txt','a+')

		tmpindex = []
		tmpbinary = []
		for i in range(len(lineindex)):
			methodName = lineindex[i].strip()
			if methodName in randomTestSuite:
				tmpindex.append(lineindex[i].strip())
				tmpbinary.append(linebinary[i].strip())

		newfileindex.write(','.join(tmpindex))
		newfilebinary.write(','.join(tmpbinary))

		newfileindex.write('\n')
		newfilebinary.write('\n')

		newfileindex.close()
		newfilebinary.close()
os.chdir('../' + 'tool')