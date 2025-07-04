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
    
def lasso(x, y, a):    
    x_matrix = numpy.transpose(numpy.asarray(x))
    y = numpy.asarray(y)
    
    clf = linear_model.Lasso(alpha = a)
    clf.fit(x_matrix, y)
    
    return clf, clf.score(x_matrix, y)
    
def ridge(x, y, a):   
    x_matrix = numpy.transpose(numpy.asarray(x))
    y = numpy.asarray(y)
    
    clf = linear_model.Ridge(alpha = a)
    clf.fit(x_matrix, y)
    
    return clf, clf.score(x_matrix, y)
    
def print_summary_stats(vars, titles):
    print("Summary statistics:")
    for i in range(len(vars)):
        print(titles[i]+" mean: "+ str(mean(vars[i])))
        print(titles[i]+" standard deviation: "+ str(standard_deviation(vars[i])), end = "\n\n")

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
    
    date_time_end = 1
    date_time_start = 0
    for i in range(2,len(sys.argv)):
        if sys.argv[i].lower().startswith("-d"):
            date_time_end = int(sys.argv[i + 1])
            try:
                date_time_start = int(sys.argv[i + 2])
            except IndexError:
                pass
        
    data_sans_time = data[0:date_time_start] + data[date_time_end:len(data)]
    #print(data)
    
    x_matrix = data_sans_time[1:]
    y = data_sans_time[0]
    
    #print(x_matrix)
    #print(y)
    
    print_summary_stats(data_sans_time, titles[0:date_time_start] + titles[date_time_end:len(titles)])
    
    if "--summary" in sys.argv:
        sys.exit()
    i = 0
    while i < n_vars-(date_time_end-date_time_start + 1):
        try:
            standardize(x_matrix[i])
            i += 1
        except ZeroDivisionError:
            print(titles[i + 1 + date_time_end - date_time_start] + " has no variation - removed from analysis")
            x_matrix = x_matrix[:i] + x_matrix[i + 1:] 
            titles = titles[:i + date_time_end - date_time_start] + titles[i + date_time_end - date_time_start + 1:]
            n_vars -= 1
            
    if not len(x_matrix):
        print("No variation in explanatory variables. Summary statistics for independent variable shown below:")
        print_summary_stats([y], titles)
        sys.exit()
    
    standardize(y)
    
    lasso_alpha = ridge_alpha = 0.001
    if len(sys.argv) > 2:
        try:
            lasso_alpha = ridge_alpha = float(sys.argv[2])
            if len(sys.argv) > 3:
                ridge_alpha = float(sys.argv[3])
        except ValueError:
            pass
    
    print("Using least-squares regression:")
    result = least_squares(x_matrix, y)
    coefs = result[0]
    print("Intercept: " + str(coefs[-1]))
    for i in range(len(coefs)-1):
        print("Coefficient for " + titles[i+date_time_end-date_time_start+1] + ": " + str(coefs[i]))
        
    print(str(result[2]) + "% of the variation in the dependent variable \
can be explained by variation in the independent variables")

    print("\nUsing Lasso regression with alpha = " + str(lasso_alpha) + ":")
    result, score = lasso(x_matrix, y, lasso_alpha)
    coefs = result.coef_
    #print(coefs)
    intercept = result.intercept_
    
    print("Intercept: " + str(intercept))
    for i in range(len(coefs)):
        print("Coefficient for " + titles[i+date_time_end-date_time_start+1] + ": " + str(coefs[i]))
        
    print(str(int(score * 10000)/100) + "% of the variation in the dependent variable \
can be explained by variation in the independent variables")

    print("\nUsing Ridge regression with alpha = " + str(ridge_alpha) + ":")
    result, score = ridge(x_matrix, y, ridge_alpha)
    coefs = result.coef_
    #print(coefs)
    intercept = result.intercept_
    
    print("Intercept: " + str(intercept))
    for i in range(len(coefs)):
        print("Coefficient for " + titles[i+date_time_end-date_time_start+1] + ": " + str(coefs[i]))
        
    print(str(int(score * 10000)/100) + "% of the variation in the dependent variable \
can be explained by variation in the independent variables")

main()    