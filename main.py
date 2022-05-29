import sys

def stripPun(word):
    # look for period
    if "." in word:
        word = word.replace(".", "")
    # look for exclamation
    elif "!" in word:
        word = word.replace("!", "")
    # look for question mark
    elif "?" in word:
        word = word.replace("?", "")
    # look for comma
    elif "," in word:
        word = word.replace(",", "")
    # look for apostrophe
    elif "'" in word:
        word = word.replace("'", "")
    elif "(" in word:
        word = word.replace("(", "")
    elif ")" in word:
        word = word.replace(")", "")
    return word.lower()


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
  #print(item)
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

# pre-processing

# 1. strip the punctuation
train_sent = []
for item in train_data:
    # seperate each sentence into words
    if "\n" in item:
        item = item.replace("\n", " ")
    if "0" in item:
        item = item.replace("0", " ")
    if "1" in item:
        item = item.replace("1", " ")
    if "\t" in item:
        item = item.replace("\t", " ")
    sentence = item.split(" ")
    # remove any empty strings in sentence
    sentence = list(filter(None, sentence))
    train_sent.append(sentence)

# 2. form the vocabulary (set of words in training data)
vocab = []
for s in train_sent:
    for word in s:
        vocab.append(stripPun(word))
print(vocab)
# 3. convert training and test data

# 4. output data to two files



# naive bayes classifier