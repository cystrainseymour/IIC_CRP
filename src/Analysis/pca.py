import sys
import math
import numpy.linalg

def mean(var):
    total = 0
    for i in var:
        total += i
    return total/len(var)    

def covariance_matrix(vars):
    n = len(vars[0])
    n_vars = len(vars)
    
    means = []
    for i in vars:
        means.append(mean(i))
    
    matrix = []
    
    total = 0
    for i in range(n_vars):
        matrix.append([])
        for j in range(n_vars):
            if i == j:
                matrix[i].append(1)
            else:
                total = 0
                for k in range(n):
                    total += (vars[i][k] - means[i]) * (vars[j][k] - means[j])
                matrix[i].append(total/(n-1))
            
            
    return matrix
    
def standard_deviation(var):
    var_mean = mean(var)
    total = 0
    for i in var:
        total += math.pow(i - var_mean, 2)
    return math.sqrt(total/(len(var)-1))
    
def normalize(var):
    stddev = standard_deviation(var)
    mean_var = mean(var)
    for i in range(len(var)):
        var[i] = (var[i] - mean_var)/stddev
        
def apply_eigenvector(vec, vars):
    rotated_data = []
    n_vars = len(vars)
    n = len(vars[0])
    #print(n)
    for i in range(n):
        total = 0
        for j in range(n_vars):
            total += vars[j][i] * vec[j]
        rotated_data.append(total)
    return rotated_data

def print_covariance(titles, covar):
    
    print("Covariance Matrix:")
    for i in titles:
        print("\t" + i, end = "")
    for i in range(len(covar)):
        print("\n" + titles[i], end = ":\t")
        for j in range(len(covar)):
            print(covar[j][i], end = "\t")
    print("")

def print_eigens(values, vectors):
    
    print("Eigenvalues:")

    for i in values:
        print("\t" + str(i), end = "")
        
    print("\nEigenvectors:")
    
    for i in range(len(vectors)):
        for j in range(len(vectors)):
            print(vectors[j][i], end = "\t")
        print("")
        
def main():
    inp_name = sys.argv[1]
    outp_name = sys.argv[2]
    npcs = int(sys.argv[3]) # number of principal components desired
    
    inp = open(inp_name, "r")
    titles = inp.readline().split("\t")
    n_vars = len(titles) - 1
    
    if npcs > n_vars:
        npcs = input("There can be at most "+n_vars + " principal components for this data. Please enter a new value:")
    
    #print(titles)
    
    vars = []
    
    try:
        while(True):
            line = inp.readline().split("\t")
            if(len(line) == 1):
                break
            for i in range(n_vars+1):
                try:
                    vars[i].append(float(line[i]))
                except IndexError:
                    #print(line[i]) load-bearing print statement? - fixed
                    vars.append([])
                    try:
                        vars[i].append(float(line[i]))
                    except ValueError:
                        vars[i].append(line[i])
                except ValueError:
                    vars[i].append(line[i])
    except EOFError:
        pass
    except IndexError:
        pass    
    
    vars_minus_time = vars[1:]
    #print(vars_minus_time)
    
    for var in vars_minus_time:
        normalize(var)
    
    covar = covariance_matrix(vars_minus_time)
    
    print_covariance(titles[1:], covar)
    
    eigval, eigvec = numpy.linalg.eig(covar)
    
    #print(eigval, "\n", eigvec)
    
    print_eigens(eigval, eigvec)
    
    highest_npcs_eigvecs = []
    highest = 0
    taken = []
    for j in range(n_vars):
        taken.append(0)
        
    for i in range(npcs):
        if i:
            highest = eigval[highest_npcs_eigvecs[-2]]
        for j in range(n_vars):
            #print(eigval[j], highest)
            if (not taken[j]) and eigval[j] > highest:
                highest_npcs_eigvecs.append(j)
                highest = eigval[j]
                taken[j] = 1
    
    rotated_data = []
    for i in range(npcs):
        rotated = apply_eigenvector(eigvec[highest_npcs_eigvecs[i]],vars_minus_time)
        try:
            for j in range(len(rotated)):
                rotated_data[j].append(rotated[j])
        except:
            for j in range(len(rotated)):
                rotated_data.append([])
                rotated_data[j].append(rotated[j])
                
    with open(outp_name, "w+") as file:
        for i in range(len(rotated_data)):
            for j in range(npcs):
                file.write(str(rotated_data[i][j]))
                if j + 1<npcs:
                    file.write(", ")
            file.write("\n")
    
main()