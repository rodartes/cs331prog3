# CS 331 Spring 2022
# Programming Assignment 3
# Team: Jane Kuffler (kufflerj@oregonstate.edu) 
#       Rose Rodarte (rodartes@oregonstate.edu)

import sys

if len(sys.argv) != 3:
    print("Error! Please enter 'main.py training-file test-file'")
    exit(1)

# open training set
train = open(sys.argv[1], "r")
# read data
train_data = []
for line in train:
    train_data.append(train.readline())
#for item in train_data:
#    print(item)
train.close()

# open test set
test = open(sys.argv[2], "r")
# read data
test_data = []
for line in test:
    test_data.append(test.readline())
#for item in test_data:
    #print(item)
test.close()

# Pre-Processing

# Naive Bayes Classifier