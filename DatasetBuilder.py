#!/usr/bin/python
# -*- coding: utf-8 -*- 
# 

import json
import datetime
from peewee import *
import Models as Model

class DatasetBuilder(object):

	# 
	# 
	# 
	def __init__(self, schoolname):

		self.db = database = SqliteDatabase('database.db')
		self.schoolname = schoolname.decode('utf-8')
		self.googleFlueFile = 'fluetrends.json'

		# Fetch school
		for school in Model.School().raw('SELECT * FROM school WHERE name=?', unicode(self.schoolname)):
			self.school = school

		print '\nIncome Rate: ', len(self.getIncomeRate(['2012-01-01', '2012-02-01']))
		print 'Outcome Rate: ', len(self.getOutcomeRate(['2012-01-01', '2012-02-01']))
		print 'Incest Rate: ', len(self.getIncestRate(['2005-01-01', '2021-01-01']))

		print '\nInfected Income Rate: ', len(self.getInfectedIncomingRate(['2005-01-01', '2021-01-01']))
		print 'Infected Outcome Rate: ', len(self.getInfectedOutgoingRate(['2005-01-01', '2021-01-01']))
		print 'Infected Incest Rate: ', len(self.getInfectedIncestRate(['2005-01-01', '2021-01-01']))

		print self.getFlueTrendsRate(['2013-01-01', '2013-02-01'])

	# 
	# 
	# 
	def createDataSection(self):

		section = []

		pass

	# 
	# Returns a list with all incoming links to this school
	# 
	def getIncomeRate(self, timeInterval):

		departments = [d for d in Model.Department.raw('SELECT * FROM department WHERE school_id=?', self.school.id)]
		links = []
		for d in departments:
			for w in Model.DepartmentWeights.raw('SELECT * FROM departmentweights WHERE destination_id=? AND owner_id != ? AND fromdate>=Datetime(?) AND todate>Datetime(?)', d.id, d.id, timeInterval[0], timeInterval[1]):
				links.append(w)

		return links

	# 
	# Returns a list with all outgoing links from this school
	# 
	def getOutcomeRate(self, timeInterval):
		departments = [d for d in Model.Department.raw('SELECT * FROM department WHERE school_id=?', self.school.id)]
		links = []
		for d in departments:
			for w in Model.DepartmentWeights.raw('SELECT * FROM departmentweights WHERE owner_id=? AND destination_id != ? AND fromdate>=Datetime(?) AND todate>Datetime(?);', d.id, d.id, timeInterval[0], timeInterval[1]):
				links.append(w)

		return links

	# 
	# Returns a list with all links within the school
	# 
	def getIncestRate(self, timeInterval):

		departments = [d for d in Model.Department.raw('SELECT * FROM department WHERE school_id=?', self.school.id)]
		links = []
		for d in departments:
			for w in Model.DepartmentWeights.raw('SELECT * FROM departmentweights WHERE owner_id=? AND destination_id=? AND fromdate>=Datetime(?) AND todate>=Datetime(?)', d.id, d.id, timeInterval[0], timeInterval[1]):
				links.append(w)

		return links

	# 
	# Returns a list with all incoming links that is potentialy infected
	# 
	def getInfectedIncomingRate(self, timeInterval):
		links = []
		for w in self.getIncomeRate(timeInterval):
			if self.getInfectionRate(w, timeInterval):
				links.append(w)

		return links

	# 
	# Returns a list with all outgoing links that is potentially infected
	# 
	def getInfectedOutgoingRate(self, timeInterval):

		links = []

		for w in self.getOutcomeRate(timeInterval):
			if self.getInfectionRate(w, timeInterval):
				links.append(w)

		return links

	# 
	# Returns a list with all links within a school that is potentially infected
	# 
	def getInfectedIncestRate(self, timeInterval):

		links = []
		for w in self.getIncestRate(timeInterval):
			if self.getInfectionRate(w, timeInterval):
				links.append(w)

		return links

	# 
	# Check if links are possible infected
	# 
	def getInfectionRate(self, w, timeInterval):
		c = self.db.execute_sql('SELECT COUNT() FROM absence WHERE child_id=? AND date>=Datetime(?) AND date<=Datetime(?)', (w.childOwner.id, timeInterval[0], timeInterval[1]))

		x = [x for x in c]

		if x[0][0] is not 0:
			return True
		return False

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

	# 
	# 
	# 
	def getFlueTrendsRate(self, timeInterval):
		data = self.getFlueTrends()
		dps = []
		for dp in data:
			date = datetime.datetime.strptime(dp['date'], '%Y-%m-%d')

			if date >= datetime.datetime.strptime(timeInterval[0], '%Y-%m-%d') and date <= datetime.datetime.strptime(timeInterval[1], '%Y-%m-%d'):
				dps.append(dp)
		
		return dps