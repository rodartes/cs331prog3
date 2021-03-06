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
train.close()

# open test set
test = open(sys.argv[2], "r")
# read data
test_data = test.readlines()
test.close()

# FIRST PART - Pre-processing

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

test_sent = []
for item in test_data:
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
    test_sent.append(sentence)


# 2. form the vocabulary (set of words in training data)
vocab = []
for s in train_sent:
    for word in s:
        if word != '0' and word != '1':
            w = stripPun(word)
            if w not in vocab:
                vocab.append(w)
vocab.sort()

# 3. convert training and test data to set features
# m = size of vocabulary
m = len(vocab)
# convert each sentence into a feature vector
train_vector = []
for s in train_sent:
    v = [0] * (m+1)
    for x in range(m):
        for w in s:
            if w.lower() == vocab[x]:
                v[x] = 1
    v[m] = s[-1]
    train_vector.append(v)

test_vector = []
for s in test_sent:
    v = ['0'] * (m+1)
    for x in range(m):
        for w in s:
            if w.lower() == vocab[x]:
                v[x] = '1'
    v[m] = s[-1]
    test_vector.append(v)


# 4. output data to two files
# add classlabel as a dummy word
vocab.append("classlabel")
# turn array of words into a string
v_list = ' '.join(str(v) for v in vocab)
ptrain = open("preprocessed_train.txt", "w")
ptrain.write(v_list)
ptrain.write("\n")
# write feature vectors
for i in train_vector:
    i = str(i)
    i = i.replace("[", "")
    i = i.replace("]", "")
    i = i.replace("'", "")
    ptrain.write(i)
    ptrain.write("\n")
ptrain.close()

ptest = open("preprocessed_test.txt", "w")
ptest.write(v_list)
ptest.write("\n")
# write feature vectors
for i in test_vector:
    i = str(i)
    i = i.replace("[", "")
    i = i.replace("]", "")
    i = i.replace("'", "")
    ptest.write(i)
    ptest.write("\n")
ptest.close()

# SECOND PART - Naive Bayes Classifier

#takes in the vocab, training set, and training feature vector and calculates the uniform dirichlet priors for every word (both pos and neg)
def train(v_list, train_vector, dirichletPos, dirichletNeg):
    numPos = 0
    numNeg = 0
    numWords = len(v_list)
    numSents = len(train_vector[0])
    
    for x in range(0, len(train_vector)):
        if train_vector[x][-1] == str(1):
            #count number of positive reviews from training set
            numPos = numPos + 1
        else:
            #count number of negative reviews from training set
            numNeg = numNeg + 1

    for word in range (0, numWords):
        existsP = 0
        for obj in train_vector:
            #Count num reviews with word and positive class label
            if obj[word] == 1 and obj[-1] == str(1):
                existsP = existsP + 1
        #calculate num+1/numPos+2 and append to dirichletPos
        dirichletPos.append(round((existsP+1)/(numPos+2), 6))
    #print(dirichletPos[0])

    for word in range (0, numWords):
        existsN = 0
        for obj in train_vector:
            #Count num reviews with word and negative class label
            if obj[word] == 1 and obj[-1] == str(0):
                existsN = existsN + 1
        #calculate num+1/numNeg+2 and append to dirichletNeg
        dirichletNeg.append((existsN+1)/(numNeg+2))
    #print(dirichletNeg[0])

def test(dirichletPos, dirichletNeg, test_vector, v_list):
    #print(test_vector[0])
    predicted = []
    for obj in test_vector:
        temp = []
        totalPos = 0
        totalNeg = 0
        #Get each word and idx of each word by sentence
        for word in range (0, len(v_list)):
            if obj[word] == str(1):
                temp.append(v_list[word])
                temp.append(word)
        #calculate positive and negative dirichlet priors for all words in sentence
        for x in range(1, len(temp), 2):
            totalPos = totalPos + dirichletPos[x] 
            totalNeg = totalNeg + dirichletNeg[x]
        # if positive is higher set 1 else set 0
        if totalPos > totalNeg:
            predicted.append(1)
        else:
            predicted.append(0)
    print(predicted)
    return predicted

def accuracy (predicted, test_vector):
    count = 0
    result = 0
    for obj in test_vector:
        if str(predicted[count]) == str(obj[-1]):
            result = result + 1
        count = count + 1

    percentRight = (result / count)*100
    return percentRight

res = open("results.txt", "w")
# same training and test data from trainingSet.txt
dirichletPos = []
dirichletNeg = []
train(vocab, train_vector, dirichletPos, dirichletNeg)
result = test(dirichletPos, dirichletNeg, train_vector, vocab)
a = round(accuracy(result, train_vector), 2)
res.write("Training and Testing on Training Set Accuracy: " + str(a) + "% \n")
# unique training and test data from trainingSet.txt and testSet.txt
dirichletPos = []
dirichletNeg = []
train(vocab, train_vector, dirichletPos, dirichletNeg)
result = test(dirichletPos, dirichletNeg, test_vector, vocab)
a = round(accuracy(result, test_vector), 2)
res.write("Training and Testing on Different Sets Accuracy: " + str(a) + "% \n")
res.close()