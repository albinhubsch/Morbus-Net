#!/usr/bin/python
# -*- coding: utf-8 -*- 
# 

import time
import sys

# Import pybrain stuff
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.datasets import SupervisedDataSet

import numpy as np
import pylab as pl
from scipy import stats

from sklearn import linear_model
from sklearn.linear_model import BayesianRidge, LinearRegression

# from pybrain import *
import DatasetBuilder as DB
from peewee import *
import Models as Model

# 
# 
# 
def createAnswerSection(ds):
	return [ds[0], ds[1], ds[2], ds[3], ds[4]]

# 
# 
# 
def intializeDataset(dataset):

	data = SupervisedDataSet(12,5)

	for index, section in enumerate(dataset):
		try:
			data.addSample( tuple(section), tuple(createAnswerSection( dataset[index + 1] )) )
		except Exception as e:
			print 'end'

	return data

# 
# 
# 
def training(d):
	n = buildNetwork(d.indim, 12, d.outdim, recurrent=False, hiddenclass=TanhLayer)
	t = BackpropTrainer(n, d, learningrate = 0.01, verbose=True)

	# trainer.trainUntilConvergence()

	for epoch in range(0,2900):
		t.train()
	return t

# 
# 
# 
def test(trained, dataset):
	testdata = SupervisedDataSet(12,5)

	for index, section in enumerate(dataset):
		try:
			testdata.addSample( tuple(section), tuple(createAnswerSection( dataset[index + 1] )) )
		except Exception as e:
			print 'end'

	trained.testOnData(testdata, verbose= True)

# 
# 
# 
if __name__ == "__main__":

	# Start timer
	start = time.time()

	# Check if all parameters is given
	if sys.argv is None or len(sys.argv) <= 2:
		print 'All parameters not set.'
		print 'This is what I need: Schoolname mode'
		exit(0)

	if sys.argv[2] is '1':
		# 
		d = DB.DatasetBuilder(sys.argv[1])
		train_data = d.getDataSet(['2012-10-01', '2014-01-31'])
		test_data = d.getDataSet(['2014-02-03', '2014-02-21'])

		trainingData = intializeDataset(train_data)
		trained = training(trainingData)
		test(trained, test_data)

	elif sys.argv[2] is '2':
		print 'hej'


	# Calculate timed program
	print "\nProgram took", time.time() - start, "seconds to run."