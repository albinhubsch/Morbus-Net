#!/usr/bin/python
# -*- coding: utf-8 -*-
from peewee import *

'''
	BaseModel


'''
class BaseModel(Model):
	class Meta:
		database = SqliteDatabase('database.db')
'''
	Child

	
'''
class Child(BaseModel):
	id = IntegerField(primary_key=True, index=True, unique=True)
	birthdate = CharField()
	sex = CharField()
	name = CharField()

'''
	Absence

	
'''
class Absence(BaseModel):
	id = IntegerField(primary_key=True, index=True, unique=True)
	child = ForeignKeyField(Child, related_name='absences')
	date = CharField()
	msg = TextField(null=True)
	fromtime = CharField(null=True)
	totime = CharField(null=True)
	category = CharField(null=True)

'''
	School

	
'''
class School(BaseModel):
	id = IntegerField(primary_key=True, index=True, unique=True)
	name = CharField()
	adress = CharField()

'''
	Department

	
'''
class Department(BaseModel):
	id = IntegerField(primary_key=True, index=True, unique=True)
	name = CharField()
	school = ForeignKeyField(School, related_name='departments')

'''
	Sibling

	
'''
class Sibling(BaseModel):
	# id = IntegerField(primary_key=True, index=True, unique=True)
	child = ForeignKeyField(Child, related_name='siblingCon', primary_key=True, index=True, unique=True)

'''
	Siblings

	
'''
class Siblings(BaseModel):
	child = ForeignKeyField(Sibling, related_name='siblings')
	sibling = ForeignKeyField(Child, related_name='siblings')

'''
	ChildDepartment

	Many to Many relation between childs and departments
'''
class ChildDepartment(BaseModel):
	id = IntegerField(primary_key=True, index=True, unique=True)
	child = ForeignKeyField(Child, related_name='departments')
	department = ForeignKeyField(Department, related_name='childs')
	fromdate = CharField(null=True)
	todate = CharField(null=True)

'''
	DeparmentsWeights

'''
class DepartmentWeights(BaseModel):
	id = IntegerField(primary_key=True, index=True, unique=True)
	owner = ForeignKeyField(Department, related_name='weights', to_field='id')
	destination = ForeignKeyField(Department, related_name='weight', to_field='id')
	fromdate = CharField(null=True)
	todate = CharField(null=True)
	childOwner = ForeignKeyField(Child, related_name='ownerWeight', to_field='id')