#!/usr/bin/python
# -*- coding: utf-8 -*- 
# 

import json
import datetime
from peewee import *
import Models as Model

# 
# DatasetBuilder
# Class builds a dataset from a specific school and timeinterval
# 
class DatasetBuilder(object):

	# 
	# A datasection looks like this
	# [m, t, w, t, f, Incoming, Outgoing, Incest, Incoming Infected, Outgoing Infected, Incest Infected, FlueTrends...]
	# 

	# 
	# Constructor
	# 
	def __init__(self, schoolname):

		self.db = database = SqliteDatabase('database.db')
		self.schoolname = schoolname.decode('utf-8')
		self.googleFlueFile = 'fluetrends.json'

		# Fetch school
		self.school = Model.School.select().where(Model.School.name == unicode(schoolname)).first()


		self.departments = [d for d in Model.Department.raw('SELECT * FROM department WHERE school_id=?', self.school.id)]

	# 
	# Return the full data set
	# 
	def getDataSet(self, timeInterval):
		dataset = []

		sdate = datetime.datetime.strptime(timeInterval[0], '%Y-%m-%d')

		while sdate <= datetime.datetime.strptime(timeInterval[1], '%Y-%m-%d'):

			sfdate = sdate + datetime.timedelta(days=4)

			dataset.append(self.createDataSection([ str(sdate.strftime("%Y-%m-%d")), str(sfdate.strftime("%Y-%m-%d")) ]))

			sdate = sdate + datetime.timedelta(days=7)
		
		return dataset

	# 
	# Create a datasection
	# 
	def createDataSection(self, timeInterval):

		print 'Creating section'

		# Add number of absences
		section = [] + self.getNumberOfAbsences(timeInterval)

		# Add incoming rate
		section.append(len(self.getIncomeRate(timeInterval)))

		# Add outgoing rate
		section.append(len(self.getOutcomeRate(timeInterval)))		

		# Add incest rate
		section.append(len(self.getIncestRate(timeInterval)))

		# Add incoming infected
		section.append(len(self.getInfectedIncomingRate(timeInterval)))

		# Add outgoing infected
		section.append(len(self.getInfectedOutgoingRate(timeInterval)))

		# Add incest infected
		section.append(len(self.getInfectedIncestRate(timeInterval)))

		# Add fluetrends
		section.append(self.getFlueTrendsRate(timeInterval)[0]['value'])

		return section

		# return [float(x)/max(section) for x in section]

	# 
	# Return number of absences for a timeinterval
	# 
	def getNumberOfAbsences(self, timeInterval):

		listOfAbsences = []

		sdate = datetime.datetime.strptime(timeInterval[0], '%Y-%m-%d')
		while sdate <= datetime.datetime.strptime(timeInterval[1], '%Y-%m-%d'):

			children = []
			absences = 0

			# 
			# What is going to happen below could be implemented as a single SQL query but
			# I honestly dont know sql good enough...
			# 
			for department in self.departments:
				for childCon in department.childs:
					if not childCon.child.id in children:
						# fetch all absences
						absences = absences + childCon.child.absences.where(Model.Absence.date == sdate.strftime('%Y-%m-%d')).count()
						children.append(childCon.child.id)

			listOfAbsences.append(absences)
			sdate = sdate + datetime.timedelta(1)
		
		return listOfAbsences

	# 
	# Returns a list with all incoming links to this school
	# 
	def getIncomeRate(self, timeInterval):
		links = []
		for d in self.departments:
			for w in Model.DepartmentWeights.raw('SELECT * FROM departmentweights WHERE destination_id=? AND owner_id != ? AND fromdate>=Datetime(?) AND todate>=Datetime(?)', d.id, d.id, timeInterval[0], timeInterval[1]):
				links.append(w)

		return links

	# 
	# Returns a list with all outgoing links from this school
	# 
	def getOutcomeRate(self, timeInterval):
		links = []
		for d in self.departments:
			for w in Model.DepartmentWeights.raw('SELECT * FROM departmentweights WHERE owner_id=? AND destination_id != ? AND fromdate>=Datetime(?) AND todate>=Datetime(?);', d.id, d.id, timeInterval[0], timeInterval[1]):
				links.append(w)

		return links

	# 
	# Returns a list with all links within the school
	# 
	def getIncestRate(self, timeInterval):
		links = []
		for d in self.departments:
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
	# Open google Flue trends file and return content
	# 
	def getFlueTrends(self):
		f = open(self.googleFlueFile)
		data = json.load(f)
		f.close()
		return data

	# 
	# Return flue trend for timeInterval
	# 
	def getFlueTrendsRate(self, timeInterval):
		data = self.getFlueTrends()
		dps = []
		for dp in data:
			date = datetime.datetime.strptime(dp['date'], '%Y-%m-%d')

			if date >= datetime.datetime.strptime(timeInterval[0], '%Y-%m-%d') and date <= datetime.datetime.strptime(timeInterval[1], '%Y-%m-%d') + datetime.timedelta(days=6):
				dps.append(dp)
		
		return dps