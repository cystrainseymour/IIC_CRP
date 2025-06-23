import numpy
import sys

def least_squares(x, y):
    x_matrix = numpy.transpose(numpy.asmatrix(x))
    #print(x_matrix, numpy.shape(x_matrix))
    y = numpy.asarray(y)
    #print(y, numpy.shape(y))
    return numpy.linalg.lstsq(x_matrix, y)

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
    
    coefs = least_squares(x_matrix, y)[0]
    print(coefs)

main()    