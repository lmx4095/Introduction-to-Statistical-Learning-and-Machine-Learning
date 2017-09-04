from numpy import *
import operator
from os import listdir

def distance_function(number, train_data, labels, k):
    train_data_shape = train_data.shape[0]
    list = tile(number, (train_data_shape,1)) - train_data
    distances = ((list**2).sum(axis=1))**0.5
    sorted_distances=distances.argsort()
    count={}
    for i in range(k):
        label = labels[sorted_distances[i]]
        count[label] = count.get(label,0) + 1
    sorted_class= sorted(count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class[0][0]

def change_image_to_vector(filename):
    vector = zeros((1,1024))
    file = open(filename)
    for i in range(32):
        line= file.readline()
        for j in range(32):
            vector[0,32*i+j] = int(line[j])
    return vector


def handwriting_class_test():
    class_labels = []
    train_file_list = listdir('trainingDigits')
    train_len = len(train_file_list)
    train_matrix = zeros((train_len,1024))
    for i in range(train_len):
        class_labels.append(train_file_list[i].split(',')[0].split('_')[0])
        train_matrix[i,:] = change_image_to_vector('trainingDigits/%s' % train_file_list[i])
    test_file_list = listdir('testDigits')
    error_count = 0.0
    test_len = len(test_file_list)
    for i in range(test_len):
        test_result = int(test_file_list[i].split('.')[0].split('_')[0])
        test_vector = change_image_to_vector('testDigits/%s' % test_file_list[i])
        classified_result = int(distance_function(test_vector, train_matrix, class_labels, 3))
        print("the classified result is:%d, the real answer is: %d" % (classified_result, test_result))
        if (classified_result != test_result): error_count += 1.0
    print("\nthe total number of errors is: %d" % error_count)
    print("\nthe error rate is: %f" % (error_count/float(test_len)))

def main():
    handwriting_class_test()

main()