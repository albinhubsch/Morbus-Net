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

from sklearn import linear_model
from sklearn.linear_model import BayesianRidge, LinearRegression

from peewee import *
import Models as Model

import matplotlib.dates as mdates

# 
# 
# 
def getSchoolAbsencesOverTime(school, timeInterval):

	schoolname = school.decode('utf-8')
	school = Model.School.select().where(Model.School.name == unicode(schoolname)).first()

	departments = [d for d in school.departments]

	timeline = []
	dataPoints = []

	neg = False

	s_date = timeInterval[0]
	while s_date <= timeInterval[1]:

		if s_date.isoweekday() in range(1, 6):

			# 
			timeline.append(s_date)

			cnum = 0

			# Fetch and sumarize all absences
			for d in departments:
				for c in d.childs:
					cnum = cnum + c.child.absences.where( Model.Absence.date == s_date.strftime("%Y-%m-%d") ).count()

			dataPoints.append(cnum)
			print s_date

		s_date = s_date + datetime.timedelta(days=1)

	return dataPoints, timeline

# 
# 
# 
def getAbsencesBySiblingsGroup_Unique():

	noSiblings = []
	siblings = []

	childs = []
	
	for child in Model.Child.select():

		if child.id not in childs:
			if child.siblings.count() > 0:
				siblings.append(child.absences.count())

				for sibling in child.siblings:
					childs.append(sibling.child.child.id)
			else:
				noSiblings.append(child.absences.count())

	print '\nUnique: Inga syskon: ', len(noSiblings)
	print 'Unique: Syskon: ', len(siblings)

	return noSiblings, siblings

# 
# 
# 
def getAbsencesBySiblingsGroup():

	noSiblings = []
	siblings = []
	
	for child in Model.Child.select():
		if child.siblings.count() > 0:
			siblings.append(child.absences.count())
		else:
			noSiblings.append(child.absences.count())

	print 'Inga syskon: ', len(noSiblings)
	print 'Syskon: ', len(siblings)

	return noSiblings, siblings

# 
# 
# 
def getAbsencesByNumberOfSiblings():
	X = []
	Y = []
	dataPoints = [[], [], [], []]
	
	for child in Model.Child.select():
		X.append(child.siblings.count())
		Y.append(child.absences.count())
		dataPoints[child.siblings.count()].append(child.absences.count())

	return X, Y, dataPoints

# 
# 
# 
def getAbsencesByChildByMonth():
	months = []
	startdate = datetime.datetime.strptime('2012-09-01', '%Y-%m-%d')
	enddate = datetime.datetime.strptime('2014-03-01', '%Y-%m-%d')

	while startdate <= enddate:

		month = []

		tempEnd = startdate + relativedelta(months=1)
		# 
		for child in Model.Child.select():
			absences = child.absences.where( (Model.Absence.date >= startdate.strftime('%Y-%m-%d') ) & (Model.Absence.date <= tempEnd.strftime('%Y-%m-%d') ) ).count()
			month.append(absences)

		months.append(month)

		startdate = startdate + relativedelta(months=1)

	return months

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

	data = getAbsencesBySiblingsGroup()
	data_unique = getAbsencesBySiblingsGroup_Unique()

	print '\nNo siblings: ', np.mean(data[0])
	print 'Siblings: ', np.mean(data[1])

	print scipy.stats.ttest_ind(data[1], data[0])

	print '\nUnique'
	print 'No siblings: ', np.mean(data_unique[0])
	print 'Siblings: ', np.mean(data_unique[1])

	print scipy.stats.ttest_ind(data_unique[1], data_unique[0])

	absencesByNumberOfSiblings = getAbsencesByNumberOfSiblings()


	pl.figure(1)
	pl.scatter(absencesByNumberOfSiblings[0], absencesByNumberOfSiblings[1])

	pl.figure(2)
	pl.boxplot(absencesByNumberOfSiblings[2])

	pl.figure(3)
	asdprepare = [ absencesByNumberOfSiblings[2][0], absencesByNumberOfSiblings[2][1] + absencesByNumberOfSiblings[2][2] + absencesByNumberOfSiblings[2][3] ]
	pl.boxplot(asdprepare)

	pl.figure(4)
	pl.boxplot(getAbsencesByChildByMonth())

	# pl.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')


	pl.show()

	# sAb = getSchoolAbsencesOverTime(sys.argv[1], [datetime.datetime.strptime('2012-09-01', '%Y-%m-%d'), datetime.datetime.strptime('2014-01-31', '%Y-%m-%d')])

	# # pl.plot(sAb[1], sAb[0])
	# # pl.gcf().autofmt_xdate()
	# # pl.show()

	# np.random.seed(20)
	# X = np.random.randn(len(sAb[0]), len(sAb[0]))  # Create gaussian data

	# # Create noise with a precision alpha of 50.
	# alpha_ = 50.
	# noise = stats.norm.rvs(loc=0, scale=1. / np.sqrt(alpha_), size=len(sAb[0]))


	# # Create the target
	# y = np.dot(X, sAb[0]) + noise

	# ###############################################################################
	# # Fit the Bayesian Ridge Regression
	# clf = BayesianRidge(compute_score=True)
	# clf.fit(X, y)

	# print 'PREDICTION: '
	# clf.predict([[1, 0.]])

	# ###############################################################################
	# # Plot true weights, estimated weights and histogram of the weights
	# pl.figure(figsize=(6, 5))
	# pl.title("Weights of the model")
	# pl.plot(clf.coef_, 'b-', label="Bayesian Ridge estimate")
	# pl.plot(sAb[0], 'g-', label="Ground truth")

	# pl.xlabel("Features")
	# pl.ylabel("Values of the weights")
	# pl.legend(loc="best", prop=dict(size=12))



	# pl.show()

	# Calculate timed program
	print "\nProgram took", time.time() - start, "seconds to run."