from numpy import *

def text_parse(string):
    import re
    list= re.split(r'\W*', string)
    return [word.lower() for word in list if len(word) > 2]

def create_vocabulary_list(data):
    vocabulary = set([])
    for document in data:
        vocabulary |= set(document)
    return list(vocabulary)

def words_to_vector(vocabulary_list, input):
    vector = [0]*len(vocabulary_list)
    for word in input:
        if word in vocabulary_list:
            vector[vocabulary_list.index(word)]+=1
    return vector

def train_naive_bayes(train_matrix,train_category):
    num_train_file = len(train_matrix)
    num_words = len(train_matrix[0])
    p0_1 = sum(train_category)/float(num_train_file)
    p0_nominater = ones(num_words); p1_nominater = ones(num_words)
    p0_denominater = 2.0; p1_denominater = 2.0
    for i in range(num_train_file):
        if train_category[i] == 1:
            p1_nominater += train_matrix[i]
            p1_denominater += sum(train_matrix[i])
        else:
            p0_nominater += train_matrix[i]
            p0_denominater += sum(train_matrix[i])
    p1 = log(p1_nominater/p1_denominater)
    p0 = log(p0_nominater/p0_denominater)
    return p0,p1,p0_1

def classify_naive_bayes(word_vector, p0, p1, p0_1):
    p1 = sum(word_vector * p1) + log(p0_1)
    p0 = sum(word_vector * p0) + log(1.0 - p0_1)
    if p1 > p0:
        return 1
    else:
        return 0

def spam_test():
    document_list = [];
    class_list = [];
    for i in range(1, 26):
        word_list = text_parse(open('email/spam/%d.txt' % i).read())
        document_list.append(word_list)
        class_list.append(1)
        word_list = text_parse(open('email/ham/%d.txt' % i).read())
        document_list.append(word_list)
        class_list.append(0)
    vocabulary_list = create_vocabulary_list(document_list)
    train_set = list(range(50));
    test_set = []
    for i in range(20):
        rand_index = int(random.uniform(0, len(train_set)))
        test_set.append(train_set[rand_index])
        del (train_set[rand_index])
    train_matrix = [];
    train_classes = []
    for index in train_set:
        train_matrix.append(words_to_vector(vocabulary_list, document_list[index]))
        train_classes.append(class_list[index])
    p0, p1, p_spam = train_naive_bayes(array(train_matrix), array(train_classes))
    error_count = 0
    for index in test_set:
        word_vector = words_to_vector(vocabulary_list, document_list[index])
        if classify_naive_bayes(array(word_vector), p0, p1, p_spam) != class_list[index]:
            error_count += 1
            print("classification error", document_list[index])
    print('the error rate is: ', float(error_count) / len(test_set))

def main():
    spam_test()

main()