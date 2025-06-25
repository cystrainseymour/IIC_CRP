import numpy
import sys
import copy
from sklearn import linear_model
import math

def mean(var):
    total = 0
    for i in var:
        total += i
    return total/len(var)
    
def standard_deviation(var):
    var_mean = mean(var)
    total = 0
    for i in var:
        total += math.pow(i - var_mean, 2)
    return math.sqrt(total/(len(var)-1))
    
def standardize(var):
    stddev = standard_deviation(var)
    mean_var = mean(var)
    for i in range(len(var)):
        var[i] = (var[i] - mean_var)/stddev

def least_squares(x, y):
    x_copy = copy.deepcopy(x)
    x_copy.append([1]*len(x[0]))
    
    x_matrix = numpy.transpose(numpy.asmatrix(x_copy))
    #print(x_matrix, numpy.shape(x_matrix))
    y = numpy.asarray(y)
    #print(y, numpy.shape(y))
    return numpy.linalg.lstsq(x_matrix, y)
    
def lasso(x, y):    
    x_matrix = numpy.transpose(numpy.asarray(x))
    y = numpy.asarray(y)
    
    clf = linear_model.Lasso(alpha = 0.001)
    clf.fit(x_matrix, y)
    
    return clf

def main():
    inp = open(sys.argv[1], "r")
    titles = inp.readline().strip().split("\t")
    n_vars = len(titles)
    
    data = []
    
    try:
        while(True):
            line = inp.readline().strip().split("\t")
            #print(line)
            try:
                for i in range(n_vars):
                    try:
                        data[i].append(float(line[i]))
                    except ValueError:
                        data[i].append(line[i])
            except IndexError:
                if line[0] == "":
                    raise EOFError
                for i in range(n_vars):
                    try:
                        data.append([float(line[i])])
                    except ValueError:
                        data.append([line[i]])
    except EOFError:
        pass
    
    data_sans_time = data[1:]
    
    x_matrix = data_sans_time[1:]
    y = data_sans_time[0]
    
    #print(x_matrix)
    #print(y)
    
    print("Using least-squares regression:")
    result = least_squares(x_matrix, y)
    coefs = result[0]
    print("Intercept: " + str(coefs[-1]))
    for i in range(len(coefs)-1):
        print("Coefficient for " + titles[i+2] + ": " + str(coefs[i]))
        
    print(str(result[2]) + "% of the variation in the dependent variable \
can be explained by variation in the independent variables")
    
    for var in x_matrix:
        standardize(var)
    standardize(y)

    print("\nUsing Lasso regression:")
    result = lasso(x_matrix, y)
    coefs = result.coef_
    #print(coefs)
    intercept = result.intercept_
    
    print("Intercept: " + str(intercept))
    for i in range(len(coefs)):
        print("Coefficient for " + titles[i+2] + ": " + str(coefs[i]))

main()    