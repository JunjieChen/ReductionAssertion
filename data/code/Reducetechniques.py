import random
from bitarray import bitarray
from gurobipy import *
import os
import sys
import subprocess as subp
import thread

subject = sys.argv[1]
os.chdir('../' + subject)

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
'''
def greedy(Name, covVectory):
	coverageBinary = covVectory.split(',')
	coverageData = []
	for line in coverageBinary:
		coverageData.append(bitarray(line.strip()))
	candidate = [i for i in range(len(coverageData))]
	picked = []
	
	tmp =  bitarray(len(coverageData[0]))
	tmp.setall(False)
	for j in range(len(coverageData)):
		tmp = tmp | coverageData[j]

	total =  bitarray(len(coverageData[0]))
	total = tmp

	while total.any():
		maxCount = 0
		pickId = 0
		for i in range(len(candidate)):
			tmpCount = (coverageData[candidate[i]] & total).count()
			if tmpCount > maxCount:
				pickId = i
				maxCount = tmpCount
		total = total ^ (coverageData[candidate[pickId]] & total)
		picked.append(candidate[pickId])
		del candidate[pickId]
	greedyResult = file('./faulttracer-files/randomGen/' + Name + 'GreedyResult.txt', 'a+')
	tmpresult = []
	for res in picked:
		tmpresult.append(str(res))
	greedyResult.write(','.join(tmpresult) + '\n')

	greedyResult.close()
'''

def GE(Name, covVectory):
	coverageBinary = covVectory.split(',')
	coverageData = []
	for line in coverageBinary:
		coverageData.append(bitarray(line.strip()))
	candidate = []
	picked = []
	colomnLength = len(coverageData[0])

	tmp =  bitarray(colomnLength)
	tmp.setall(False)
	for j in range(len(coverageData)):
		tmp = tmp | coverageData[j]

	total =  bitarray(colomnLength)
	total = tmp

	for j in range(colomnLength):
		count1 = 0
		enssial = -1
		for i in range(len(coverageData)):
			if coverageData[i][j] == 1:
				count1 += 1
				enssial = i
			if count1 > 1:
				break
		if count1 == 1 and enssial != -1 and enssial not in picked:
			picked.append(enssial)
	for value in picked:
		total = total ^ (coverageData[value] & total)
	for i in range(len(coverageData)):
		if i not in picked:
			candidate.append(i)
	while total.any():
		maxCount = 0
		pickId = 0
		for i in range(len(candidate)):
			tmpCount = (coverageData[candidate[i]] & total).count()
			if tmpCount > maxCount:
				pickId = i
				maxCount = tmpCount
		total = total ^ (coverageData[candidate[pickId]] & total)
		picked.append(candidate[pickId])
		del candidate[pickId]
	GEResult = file('./coverageFiles/randomGen/' + Name + 'GEResult.txt', 'a+')
	tmpresult = []
	for res in picked:
		tmpresult.append(str(res))
	GEResult.write(','.join(tmpresult) + '\n')
	GEResult.close()


def GRE(Name, covVectory):
	coverageBinary = covVectory.split(',')
	coverageData = []
	for line in coverageBinary:
		coverageData.append(bitarray(line.strip()))
	tmpCandidate = []
	candidate = []
	picked = []
	redundant = []

	tmp =  bitarray(len(coverageData[0]))
	tmp.setall(False)
	for j in range(len(coverageData)):
		tmp = tmp | coverageData[j]

	total =  bitarray(len(coverageData[0]))
	total = tmp

	for i in range(len(coverageData)):
		for j in range(len(coverageData)):
			if i == j:
				continue
			if coverageData[i] == coverageData[j]:
				if i > j and i not in redundant:
					redundant.append(i)
				elif i < j and j not in redundant:
					redundant.append(j)
			elif (coverageData[i] & coverageData[j] == coverageData[i]) and i not in redundant:
				redundant.append(i)
	for i in range(len(coverageData)):
		if i not in redundant:
			tmpCandidate.append(i)
	colomnLength = len(coverageData[0])
	for j in range(colomnLength):
		count1 = 0
		enssial = -1
		for i in range(len(tmpCandidate)):
			if coverageData[tmpCandidate[i]][j] == 1:
				count1 += 1
				enssial = tmpCandidate[i]
			if count1 > 1:
				break
		if count1 == 1 and enssial != -1 and enssial not in picked:
			picked.append(enssial)
	for value in picked:
		total = total ^ (coverageData[value] & total)
	for i in range(len(coverageData)):
		if i not in redundant and i not in picked:
			candidate.append(i)
	print len(picked)
	while total.any():
		maxCount = 0
		pickId = 0
		for i in range(len(candidate)):
			tmpCount = (coverageData[candidate[i]] & total).count()
			if tmpCount > maxCount:
				pickId = i
				maxCount = tmpCount
		total = total ^ (coverageData[candidate[pickId]] & total)
		picked.append(candidate[pickId])
		del candidate[pickId]
	GREResult = file('./coverageFiles/randomGen/' + Name + 'GREResult.txt', 'a+')
	tmpresult = []
	for res in picked:
		tmpresult.append(str(res))
	GREResult.write(','.join(tmpresult) + '\n')
	GREResult.close()

def getWinner(i, j, tmpRequirements, coverageData):
	if (coverageData[i] & tmpRequirements).count() == (coverageData[j] & tmpRequirements).count():
		return (False, -1)
	elif (coverageData[i] & tmpRequirements).count() > (coverageData[j] & tmpRequirements).count():
		return (True, i)
	else:
		return (True, j)

def HGS(Name, covVectory):
	flag1 = 0###
	coverageBinary = covVectory.split(',')
	coverageData = []
	for line in coverageBinary:
		coverageData.append(bitarray(line.strip()))
	picked = []
	colomnLength = len(coverageData[0])

	tmp =  bitarray(colomnLength)
	tmp.setall(False)
	for j in range(len(coverageData)):
		tmp = tmp | coverageData[j]

	total =  bitarray(colomnLength)
	total = tmp

	T = [[] for i in range(colomnLength)]
	for j in range(colomnLength):
		for i in range(len(coverageData)):
			if coverageData[i][j] == 1:
				T[j].append(i)
	coverNum = dict()
	for i in range(len(T)):
		length = len(T[i])
		if length == 1:
			flag1 = 1###
		if length not in coverNum:
			coverNum[length] = []
		coverNum[length].append(i)
	if flag1 == 1:###
		for tmp in coverNum[1]:
			if T[tmp][0] not in picked:
				picked.append(T[tmp][0])
				total = total ^ (coverageData[T[tmp][0]] & total)
	maxKey = max(coverNum.keys())
	currentCard = 2
	while total.any() and currentCard <= maxKey:
		requirments = bitarray(colomnLength)
		requirments.setall(False)
		candidate = []
		if currentCard not in coverNum.keys():
			currentCard += 1
			continue
		for value in coverNum[currentCard]:
			requirments[value] = 1
			for test in T[value]:
				if test not in candidate:
					candidate.append(test)
		requirments = requirments & total
		while requirments.any():
			maxCount = -1
			pickId = -1
			for i in range(len(candidate)):
				tmpCount = (coverageData[candidate[i]] & requirments).count()
				if tmpCount > maxCount and candidate[i] not in picked:
					pickId = i
					maxCount = tmpCount
				elif tmpCount == maxCount:
					tmpCard = currentCard + 1
					(winnerFlag, winner) = (False, -1)
					while tmpCard <= maxKey and not winnerFlag:
						tmpRequirements = bitarray(colomnLength)
						tmpRequirements.setall(False)
						if tmpCard not in coverNum.keys():
							tmpCard += 1
							continue
						for value in coverNum[currentCard]:
							tmpRequirements[value] = 1
							tmpRequirements = tmpRequirements & total
						(winnerFlag, winner) = getWinner(candidate[i], candidate[pickId], tmpRequirements, coverageData)
						tmpCard += 1
					if winnerFlag == True:
						if winner == 0:
							pickId = i
					else:
						randInt = random.randint(0, 1)
						pickId = (randInt % 2) * pickId + ((randInt + 1) % 2) * i
			total =	total ^ (coverageData[candidate[pickId]] & total)
			requirments = requirments ^ (coverageData[candidate[pickId]] & requirments)
			picked.append(candidate[pickId])
			del candidate[pickId]
		currentCard += 1
	HGSResult = file('./coverageFiles/randomGen/' + Name + 'HGSResult.txt', 'a+')
	tmpresult = []
	for res in picked:
		tmpresult.append(str(res))
	HGSResult.write(','.join(tmpresult) + '\n')
	HGSResult.close()

def ILP(Name, covVectory):
	coverageBinary = covVectory.split(',')
	coverageData = []
	for line in coverageBinary:
		coverageData.append(bitarray(line.strip()))

	colomnLength = len(coverageData[0])
	tmp =  bitarray(colomnLength)
	tmp.setall(False)
	for j in range(len(coverageData)):
		tmp = tmp | coverageData[j]

	total =  bitarray(colomnLength)
	total = tmp

	m = Model('ILP')
	length = len(coverageData)
	var = [0 for i in range(length)]
	for i in range(length):
		var[i] = m.addVar(vtype = GRB.BINARY, name='x' + str(i))
	m.update()
	selectTestNum = LinExpr()
	for i in range(length):
		selectTestNum += var[i]
	m.setObjective(selectTestNum, GRB.MINIMIZE)

	requirmentsNum = len(coverageData[0])
	for i in range(requirmentsNum):
		tmpConstr = LinExpr()
		for j in range(length):
			tmpConstr += coverageData[j][i] * var[j]
		m.addConstr(tmpConstr >= total[i], 'c' + str(i))
	m.optimize()
	ILPResult = file('./coverageFiles/randomGen/' + Name + 'ILPResult.txt', 'a+')
	tmpresult = []
	for v in m.getVars():
		if v.x > 0.5:
			tmpresult.append(v.varName.split('x')[-1])
	ILPResult.write(','.join(tmpresult) + '\n')
	ILPResult.close()


def reduction(Name, covVectory):
	#greedy(Name, covVectory)
	GE(Name, covVectory)
	GRE(Name, covVectory)
	HGS(Name, covVectory)
	ILP(Name, covVectory)

repeatTimes = 1000

coverages = ['branch', 'method', 'statement', 'mutation']
'''
for cov in coverages:
	totalResultFile = open('./faulttracer-files/randomGen/'+cov+'GreedyTotal.txt','w')
	additionalResultFile = open('./faulttracer-files/randomGen/'+cov+'GreedyAdditional.txt','w')
	GAResultFile = open('./faulttracer-files/randomGen/'+cov+'Genetic.txt','w')
	GAResultFileout = open('./faulttracer-files/randomGen/'+cov+'tmpfile.txt_output','w')
	ARPResultFile = open('./faulttracer-files/randomGen/'+cov+'ArtMaxMin.txt','w')
	totalResultFile.close()
	additionalResultFile.close()
	GAResultFile.close()
	GAResultFileout.close()
	ARPResultFile.close()
'''
branchCov = open('./coverageFiles/randomGen/branchCoverageBinary.txt')
branchCovLines = branchCov.readlines()
branchCov.close()

methodCov = open('./coverageFiles/randomGen/methodCoverageBinary.txt')
methodCovLines = methodCov.readlines()
methodCov.close()

statementCov = open('./coverageFiles/randomGen/statementCoverageBinary.txt')
statementCovLines = statementCov.readlines()
statementCov.close()


for cnt in range(repeatTimes):
	reduction('branch', branchCovLines[cnt].strip())
	reduction('method', methodCovLines[cnt].strip())
	reduction('statement', statementCovLines[cnt].strip())

'''
	tmpfileb = open('./faulttracer-files/randomGen/branchtmpfile.txt','w')
	for tmpline in branchCovLines[cnt].strip().split(','):
		tmpfileb.write(tmpline + '\n')
	tmpfileb.close()

	tmpfilem = open('./faulttracer-files/randomGen/methodtmpfile.txt','w')
	for tmpline in branchCovLines[cnt].strip().split(','):
		tmpfilem.write(tmpline + '\n')
	tmpfilem.close()

	tmpfiles = open('./faulttracer-files/randomGen/statementtmpfile.txt','w')
	for tmpline in branchCovLines[cnt].strip().split(','):
		tmpfiles.write(tmpline + '\n')
	tmpfiles.close()

	exccmd('java -cp ../prioritization/ GreedyTotal ' + './faulttracer-files/randomGen/')
	exccmd('java -cp ../prioritization/ GreedyAdditional ' + './faulttracer-files/randomGen/')
	exccmd('java -cp ../prioritization/ Genetic ' + './faulttracer-files/randomGen/')
	exccmd('java -cp ../prioritization/ ARTMaxMin ' + './faulttracer-files/randomGen/')
'''
os.chdir('../' + 'tool')