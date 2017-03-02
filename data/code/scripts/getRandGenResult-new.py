#-*-coding:utf-8-*-2
import xml.dom.minidom
import random
import shutil
import os
import copy
import sys
import numpy as np

subject = sys.argv[1]
os.chdir('../' + subject)
mutationFile = xml.dom.minidom.parse('../pit_result/'+subject+'.xml')
mutations = mutationFile.documentElement.getElementsByTagName('mutation')
candidateMutation = [i for i in range(len(mutations))]
groupedMutation = [[] for i in range(100)]
numPerGroup = 5
#repeatTimes = 10
random.shuffle(candidateMutation)
coverages = ['branch', 'method', 'statement']

'''
cnt = 0
while cnt < len(groupedMutation):
	tmp = []
	count = 0
	for j in range(numPerGroup):
		if mutations[candidateMutation[j]].getAttribute('status') == 'KILLED':
			count += 1 
	if count > 0:
		for j in range(numPerGroup):
			groupedMutation[cnt].append(candidateMutation[j])
		cnt += 1
		
	del candidateMutation[:numPerGroup]
'''
dstPath = '../result/' + subject + '/'
if os.path.exists(dstPath):
	shutil.rmtree(dstPath)
os.mkdir(dstPath)
killMap = dict()
isKilled = dict()
with open(dstPath + 'reduceKillMap.csv', 'w+') as output:
	for num in range(len(mutations)):
		if mutations[num].getAttribute('status') == 'KILLED':
			tmp = (mutations[num].getElementsByTagName('killingTest')[0].childNodes)[0].data.split(',')
			isKilled[num] = True
		else:
			tmp = []
			isKilled[num] = False
		if num not in killMap:
			killMap[num] = []
		for test in tmp:
			killMap[num].append(test.split('(')[0])
		output.write(str(num) + ',' + ','.join(killMap[num]) + '\n')
'''
with open(dstPath + 'prioritizationKillMap.csv', 'w+') as output:
	for i in range(len(groupedMutation)):
		for num in groupedMutation[i]:
			output.write(str(num) + ',' + ','.join(killMap[num]) + '\n')
'''
print 'map done'
def getKillPercent(originalTestSuite, reducedTestSuite, name, path):
	countori = 0
	countred = 0
	value = ''
	for i in range(len(mutations)):
		if not isKilled[i]:
			continue
		killedori = False
		killedred = False
		for killingtest in killMap[i]:
			if not killedori:
				for test in originalTestSuite:
					if test in killingtest:
						killedori = True
			if not killedred:
				for test in reducedTestSuite:
					if test in killingtest:
						killedred = True
		if killedori:
			countori += 1
		if killedred:
			countred += 1
	if countori == 0:
		value = 'NA'
	else:
		value = str((float(countori) - float(countred)) / float(countori))
		
	return (value + '\t' + str(float(len(reducedTestSuite)) / float(len(originalTestSuite))) + '\t' + 
		str(countred) + '\t' + str(countori) + '\n')

reductionDstPath = dstPath + 'RandomReduction/'
os.mkdir(reductionDstPath)
reductionApproachs = ['GE','GRE','HGS','ILP']


for coverage in coverages:
	indexFile = open('./coverageFiles/randomGen/' + coverage + 'Index.txt').readlines()
	for approach in reductionApproachs:
		path = reductionDstPath + coverage + approach + '/'
		os.mkdir(path)
		result = open('./coverageFiles/randomGen/' + coverage + approach + 'Result.txt').readlines()
		tmpPlot = []
		for cnt in range(len(result)):
			index = indexFile[cnt].strip().split(',')
			reduceResult = result[cnt].strip().split(',')
			testSuite = []

			for testId in reduceResult:
				if testId!='':
					testSuite.append(index[int(testId)])
			plot = getKillPercent(index, testSuite, coverage + approach, path)
			tmpPlot.append(plot)
		with open(path + coverage + approach + 'ForPlot.txt', 'a+') as output:
			output.write('value\treducedSize\treducedTestsuiteKillNum\toriginalTestsuiteKillNum\n')
			for line in tmpPlot:
				output.write(line)
		print 'done'
'''
def getAPFD(testSuite, result):
	tmpKillResult = []
	numArray = []
	if len(testSuite) != len(result):
		print 'error'
	for i in range(len(groupedMutation)):
		(count, tm) = (0, 0)
		for mutationId in groupedMutation[i]:
			killed = False
			position = 0
			while position < len(result) and not killed:
				for killingTest in killMap[mutationId]:
					if testSuite[int(result[position])] in killingTest:
						killed = True
						break
				if not killed:
					position += 1
			if killed:
				count += 1
				tm += position + 1
		if count == 0:
			tmpKillResult.append('NA')
		else:
			apfd = 1.0 / float(2*len(testSuite)) + 1 - float(tm) / (float(len(testSuite)) * float(count))
			if apfd < 0:
				print i, len(testSuite), count, tm
			tmpKillResult.append(str(apfd))
			numArray.append(apfd)
	if len(numArray) == 0:
		return (','.join(tmpKillResult) + ',NA,NA\n', 'NA\tNA\t' + str(len(testSuite)) + '\n')
	arrayForCount = np.array(numArray)
	return (','.join(tmpKillResult) + ',' + str(np.mean(arrayForCount)) + ',' 
		+ str(np.median(arrayForCount)) +'\n', str(np.mean(arrayForCount)) + '\t' + 
		str(np.median(arrayForCount)) + '\t' + str(len(testSuite)) + '\n')


prioritizationDstPath = dstPath + 'RandomPrioritization/'
os.mkdir(prioritizationDstPath)
prioritizationApproach = ['ArtMaxMin', 'GreedyTotal', 'GreedyAdditional', 'Genetic']

for coverage in coverages:
	indexFile = open('./faulttracer-files/randomGen/' + coverage + 'Index.txt').readlines()
	for approach in prioritizationApproach:
		path = prioritizationDstPath + coverage + approach + '/'
		os.mkdir(path)
		result = open('./faulttracer-files/randomGen/' + coverage + approach + '.txt').readlines()
		tmpData = []
		tmpPlot = []
		for cnt in range(len(result)):
			index = indexFile[cnt].strip().split(',')
			prioritizationResult = result[cnt].strip().split(',')
			(data, plot) = getAPFD(index, prioritizationResult)
			tmpData.append(data)
			tmpPlot.append(plot)
		with open(path + coverage + approach + '.csv', 'w+') as output:
			output.write(','.join([str(i+1) for i in range(len(groupedMutation))]) + ',average' + ',median' +  '\n')
			for line in tmpData:
				output.write(line)
		with open(path + coverage + approach + 'ForPlot.txt', 'a+') as output:
			output.write('average\tmedian\ttestSuiteSize\n')
			for line in tmpPlot:
				output.write(line)
		print 'done'
'''