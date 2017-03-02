import os

subjects = ['IClojure']
#'jackson-datatype-joda',,'hashids-java','commons-email','exp4j','redline-smalltalk-master','Confucius','brickhouse','clojure-maven-plugin','glacieruploader','gson-fire'
#os.mkdir('../result')
for subject in subjects:
	print subject
	#os.system('python testCaseReduce_bai.py ' + subject)
	os.system('python getRandGenResult-new.py ' + subject)