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

# from pybrain import *
import DatasetBuilder as DB
from peewee import *
import Models as Model


# 
# 
# 

def make_dataset():
    """
    Creates a set of training data.
    """
    data = SupervisedDataSet(2,1)

    data.addSample([1,1],[0])
    data.addSample([1,0],[1])
    data.addSample([0,1],[1])
    data.addSample([0,0],[0])

    return data


def training(d):
    """
    Builds a network and trains it.
    """
    n = buildNetwork(d.indim, 2, d.outdim, recurrent=False)
    t = BackpropTrainer(n, d, learningrate = 0.01, momentum = 0.99, verbose = True)
    for epoch in range(0,1000):
        t.train()
    return t


def test(trained):
    """
    Builds a new test dataset and tests the trained network on it.
    """
    testdata = SupervisedDataSet(2,1)
    testdata.addSample([1,1],[0])
    testdata.addSample([1,0],[1])
    testdata.addSample([0,1],[1])
    testdata.addSample([0,0],[0])
    trained.testOnData(testdata, verbose= True)


def run():
    """
    Use this function to run build, train, and test your neural network.
    """
    trainingdata = make_dataset()
    trained = training(trainingdata)
    test(trained)

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

    # 
    # 
    # 
    d = DB.DatasetBuilder(sys.argv[1], ['2013-01-07', '2013-05-31'])
    # run()


    # Calculate timed program
    print "\nProgram took", time.time() - start, "seconds to run."