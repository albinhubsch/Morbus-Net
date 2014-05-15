#!/usr/bin/python
# -*- coding: utf-8 -*- 
# 

import time
import sys
import datetime
from dateutil.relativedelta import relativedelta

import numpy as np
import pylab as pl
import scipy
import scipy.stats
import matplotlib as mplot

from peewee import *
import Models as Model

# CONSTANTS
TIMEINTERVAL = [datetime.datetime.strptime('2013-10-01', '%Y-%m-%d'), datetime.datetime.strptime('2013-10-14', '%Y-%m-%d')]
DATAINTERVAL = [datetime.datetime.strptime('2012-09-01', '%Y-%m-%d'), datetime.datetime.strptime('2014-01-31', '%Y-%m-%d')]

# 
# 
# 
def doCrossCorrelationBetweenChildrenAndSiblings(timeInterval):

	childIds = []

	correlation = []
	
	# Fetch absences for given time interval for child and siblings
	for child in Model.Child.select():
		if child.siblings.count() > 0:

			if child.id not in childIds:

				childD = []
				siblingsD = {}

				sdate = timeInterval[0]

				while sdate <= timeInterval[1]:
					if sdate.isoweekday() in range(1, 6):

						childD.append(child.absences.where(Model.Absence.date == sdate.strftime("%Y-%m-%d")).count())

						for sibling in child.siblings:

							if sibling.child.child.id not in childIds:
								childIds.append(sibling.child.child.id)

							try:
								siblingsD[sibling.child.child.id].append(sibling.child.child.absences.where(Model.Absence.date == sdate.strftime("%Y-%m-%d")).count())
							except KeyError:
								siblingsD[sibling.child.child.id] = [sibling.child.child.absences.where(Model.Absence.date == sdate.strftime("%Y-%m-%d")).count()]

					sdate = sdate + datetime.timedelta(days=1)

				# map(sum,zip(A,B,C))
				siblingSum = [0] * len(childD)
				for i in siblingsD:
					siblingSum = map(sum, zip(siblingSum, siblingsD[i]))
					correlation.append(np.array( np.correlate(childD, siblingsD[i], "full") ))

				print child.name, childD
				# print 'Siblings', siblingsD
				# print 'Summa', siblingSum
				# print 'Correlation', scipy.stats.pearsonr(childD, siblingSum)
				# print 'Correlation', np.correlate(childD, siblingSum, "full")
				# print 'Correlation', np.corrcoef(childD, siblingSum)
				# print '\n'


	print len(correlation[0])
	correlation_mean = np.zeros(len(correlation[0]))
	varv = 1
	for corr in correlation:
		varv = varv + 1
		correlation_mean = correlation_mean + corr


	correlation_mean = correlation_mean/varv

	return correlation_mean

# 
# 
# 
def doCrossCorrelationOverTimeChildrenAndSiblings():
	timePeriods = []
	sdate = DATAINTERVAL[0]
	while sdate <= DATAINTERVAL[1]:
		timePeriods.append(doCrossCorrelationBetweenChildrenAndSiblings([sdate, sdate + datetime.timedelta(days=14)]))
		sdate = sdate + datetime.timedelta(days=14)

	varv = 1
	tp_mean = np.zeros(len(timePeriods[0]))
	for tp in timePeriods:
		varv = varv + 1
		tp_mean = tp_mean + tp

	tp_mean = tp_mean/varv

	return tp_mean

# 
# 
# 
def doCrossCorrelationBetweenAllChildren():
	pass

# 
# 
# 
if __name__ == "__main__":

	# Start timer
	start = time.time()

	# Check if all parameters is given
	if sys.argv is None or len(sys.argv) <= 1:
		print 'All parameters not set.'
		print 'This is what I need: Schoolname'
		exit(0)

	# 
	# DO CROSS CORRELATION BETWEEN CHILDS AND SIBLINGS
	# 
	# xcorrChildSiblingsMean = doCrossCorrelationOverTimeChildrenAndSiblings()
	# pl.figure(1)
	# pl.xlabel('Time Lag')
	# pl.ylabel('Correlation Measure')
	# pl.plot(xcorrChildSiblingsMean)
	# pl.show()


	# 
	# DO CROSS CORRELATION BETWEEN DEPARTMENTS
	# 


	# 
	# DO CROSS CORRELATION BETWEEN SCHOOLS
	# 


	# 
	# DO CROSS CORRELATION BETWEEN CHILDREN
	# 


	# Calculate timed program
	print "\nProgram took", time.time() - start, "seconds to run.\n"