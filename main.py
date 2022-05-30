# CS 331 Spring 2022
# Programming Assignment 3
# Team: Jane Kuffler (kufflerj@oregonstate.edu) 
#       Rose Rodarte (rodartes@oregonstate.edu)

import sys

def stripPun(word):
    # look for period
    if "." in word:
        word = word.replace(".", "")
    # look for exclamation
    if "!" in word:
        word = word.replace("!", "")
    # look for question mark
    if "?" in word:
        word = word.replace("?", "")
    # look for comma
    if "," in word:
        word = word.replace(",", "")
    # look for apostrophe
    if "'" in word:
        word = word.replace("'", "")
    if "(" in word:
        word = word.replace("(", "")
    if ")" in word:
        word = word.replace(")", "")
    return word.lower()


if len(sys.argv) != 3:
    print("Error! Please enter 'main.py training-file test-file'")
    exit(1)

# open training set
train = open(sys.argv[1], "r")
# read data
train_data = train.readlines()
#for item in train_data:
  #print(item)
#print(train_data)
train.close()

# open test set
test = open(sys.argv[2], "r")
# read data
test_data = test.readlines()
#for line in test:
#    test_data.append(test.readline())
#for item in test_data:
    #print(item)
test.close()

# pre-processing

# 1. strip the punctuation
train_sent = []
for item in train_data:
    # seperate each sentence into words
    if "\n" in item:
        item = item.replace("\n", " ")
    #if "0" in item:
     #   item = item.replace("0", " ")
    #if "1" in item:
    #    item = item.replace("1", " ")
    if "\t" in item:
        item = item.replace("\t", " ")
    if "." in item:
        item = item.replace(".", " ")
    if "," in item:
        item = item.replace(",", " ")
    sentence = item.split(" ")
    # remove any empty strings in sentence
    sentence = list(filter(None, sentence))
    train_sent.append(sentence)

#for i in train_sent:
    #print(i)

# 2. form the vocabulary (set of words in training data)
vocab = []
for s in train_sent:
    for word in s:
        if word != '0' and word != '1':
            w = stripPun(word)
            if w not in vocab:
                vocab.append(w)
vocab.sort()
#print(vocab)

# 3. convert training and test data to set features
# m = size of vocabulary
m = len(vocab)
# convert each sentence into a feature vector


# 4. output data to two files
vocab.append("classlabel")
v_list = ' '.join(str(v) for v in vocab)
ptrain = open("preprocessed_train.txt", "w")
ptrain.write(v_list)
ptrain.close()

ptest = open("preprocessed_test.txt", "w")
ptest.write(v_list)
ptest.close()


# naive bayes classifier