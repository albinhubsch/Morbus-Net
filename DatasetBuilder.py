#!/usr/bin/python
# -*- coding: utf-8 -*- 
# 

import json
import Models as Model

class DatasetBuilder(object):

	# 
	# 
	# 
	def __init__(self, schoolname):

		self.schoolname = schoolname.decode('utf-8')
		self.googleFlueFile = 'fluetrends.json'

		# Fetch school
		for school in Model.School().raw('SELECT * FROM school WHERE name=?', unicode(self.schoolname)):
			self.school = school

		print 'Income Rate: ', len(self.getIncomeRate(['2012-01-01', '2012-02-01']))
		print 'Outcome Rate: ', len(self.getOutcomeRate(['2012-01-01', '2012-02-01']))
		print 'Incest Rate: ', len(self.getIncestRate(['2005-01-01', '2021-01-01']))

	# 
	# 
	# 
	def createDataSection(self):

		section = []

		pass

	# 
	# 
	# 
	def getIncomeRate(self, timeInterval):

		departments = [d for d in Model.Department.raw('SELECT * FROM department WHERE school_id=?', self.school.id)]
		links = []
		for d in departments:
			for w in Model.DepartmentWeights.raw('SELECT * FROM departmentweights WHERE destination_id=? AND fromdate>=Datetime(?) AND todate>Datetime(?);', d.id, timeInterval[0], timeInterval[1]):
				links.append(w)

		return links

	# 
	# 
	# 
	def getOutcomeRate(self, timeInterval):
		departments = [d for d in Model.Department.raw('SELECT * FROM department WHERE school_id=?', self.school.id)]
		links = []
		for d in departments:
			for w in Model.DepartmentWeights.raw('SELECT * FROM departmentweights WHERE owner_id=? AND fromdate>=Datetime(?) AND todate>Datetime(?);', d.id, timeInterval[0], timeInterval[1]):
				links.append(w)

		return links

	# 
	# 
	# 
	def getIncestRate(self, timeInterval):

		departments = [d for d in Model.Department.raw('SELECT * FROM department WHERE school_id=?', self.school.id)]
		links = []
		for d in departments:
			for w in Model.DepartmentWeights.raw('SELECT * FROM departmentweights WHERE owner_id=? AND destination_id=? AND fromdate>=Datetime(?) AND todate>=Datetime(?);', d.id, d.id, timeInterval[0], timeInterval[1]):
				links.append(w)

		return links

	# 
	# 
	# 
	def getInfectedIncomingRate(self, timeInterval):
		pass

	# 
	# 
	# 
	def getInfectedOutgoingRate(self, timeInterval):
		pass

	# 
	# 
	# 
	def getInfectedIncestRate(self, timeInterval):
		pass

	# 
	# 
	# 
	def getDataSet(self):
		return []

	# 
	# 
	# 
	def getFlueTrends(self):
		f = open(self.googleFlueFile)
		data = json.load(f)
		f.close()
		return data