import sys
import pandas
import numpy
import copy
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
import math
import scipy.stats as stats    
import matplotlib.pyplot as plt

def ordinary_least_squares(x, y):
    x_matrix = copy.deepcopy(x)
    x_matrix["Gradient"] = [1]*len(x_matrix)
    
    x_matrix = numpy.asmatrix(x_matrix)
    
    y = numpy.asarray(y)
    
    result = numpy.linalg.lstsq(x_matrix, y)
    coefs = result[0]
    
    predicted = []
    
    for i in range(len(x)):
        predicted.append(coefs[-1])
        for j in range(len(x.columns)):
            predicted[-1] += x[x.columns[j]][i] * coefs[j]
    
    score = result[2]/100
    
    return coefs, score, predicted
    
def lasso(x, y, a):
    x_matrix = numpy.asarray(x)
    y = numpy.asarray(y)
    
    clf = linear_model.Lasso(alpha = a)
    clf.fit(x_matrix, y)
    
    coefs = list(clf.coef_)
    coefs.append(clf.intercept_)
    score = clf.score(x_matrix, y)
    predicted = clf.predict(x_matrix)
    
    return coefs, score, predicted
    
def ridge(x, y, a):
    x_matrix = numpy.asarray(x)
    y = numpy.asarray(y)
    
    clf = linear_model.Ridge(alpha = a)
    clf.fit(x_matrix, y)
    
    coefs = list(clf.coef_)
    coefs.append(clf.intercept_)
    score = clf.score(x_matrix, y)
    predicted = clf.predict(x_matrix)
    
    
    return coefs, score, predicted
    
def f_test(predicted, y, k):
    #f - test to determine whether the variance of the predicted values came from the same distribution
    #as the variances of the values predicted using only the intercept or mean. 
    
    n = len(predicted)
    
    ndf = k - 1
    ddf = n - k
    
    total_mean = sum(y)/n
    ss_total = sum([math.pow(i - total_mean, 2) for i in y])
    
    ss_r = sum([math.pow(i - total_mean, 2) for i in predicted])
    
    ss_e = ss_total - ss_r
    
    msr = ss_r/ddf
    mse = ss_r/ndf
    
    f = mse/msr
    
    return stats.f.cdf(f, ndf, ddf)
    
    
def print_summary_stats(vars, titles):
    print("Summary statistics:")
    for i in range(len(titles)):
        if not titles[i].startswith("ONEHOT"):
            print(titles[i]+" mean: "+ str(vars.loc[:,titles[i]].mean()))
            print(titles[i]+" standard deviation: "+ str(vars.loc[:,titles[i]].std()), end = "\n\n")

def main():
    files = sys.argv[1].split(", ")
    
    data = pandas.concat(pandas.read_csv(inp, sep="\t") for inp in files)
    data.set_index(pandas.Index(range(len(data))), inplace = True)
    
    date_time_cols = ["Date", "Time", "Datetime"]
    
    for i in range(2, len(sys.argv)):
        date_time_cols.append(sys.argv[i])
    
    data_sans_time = data
    for col in date_time_cols:
        try:
            data_sans_time = data_sans_time.drop(col, axis = 1)
        except:
            pass
            
    n_vars = len(data_sans_time.columns)
    
    # print(data.head())
    # print(data.columns)
    
    x_matrix = data_sans_time.drop(data_sans_time.columns[0], axis = 1)
    y = data_sans_time[data_sans_time.columns[0]]
    
    if "onehot" in "_".join(list(map(lambda s: s.replace("_", ""), sys.argv[2:]))).lower().replace("-", ""):
        data_sans_time = data_sans_time.drop([col for col in data_sans_time.columns if col.startswith("ONEHOT")], axis=1)
    
    print_summary_stats(data_sans_time, data_sans_time.columns)
    
    if "summary" in "_".join(list(map(lambda s: s.replace("_", ""), sys.argv[2:]))).lower().replace("-", ""):
        sys.exit()
        
    for col in x_matrix.columns:
        if not x_matrix[col].std():
            x_matrix.drop(col, axis = 1, inplace = True)
            data_sans_time.drop(col, axis = 1, inplace = True)
            print(col, "has no variation -- removed from analysis\n")

    if not len(x_matrix):
        print("No variation in explanatory variables. Summary statistics for independent variable shown below:")
        print_summary_stats([y], titles)
        sys.exit()
    
    lasso_alpha = ridge_alpha = 0.001
    if len(sys.argv) > 2:
        try:
            lasso_alpha = ridge_alpha = float(sys.argv[-2])
            if len(sys.argv) > 3:
                ridge_alpha = float(sys.argv[-1])
        except ValueError:
            pass
    
    print("Using simple least-squares regression:")
    coefs, score, predicted = ordinary_least_squares(x_matrix, y)
    
    best_score = score
    best_pred = predicted
    best_coefs = coefs
    
    print("Intercept: " + str(coefs[-1]))
    for i in range(len(coefs)-1):
        print("Coefficient for " + x_matrix.columns[i] + ": " + str(coefs[i]))
        
    print(str(int(score * 10000)/100) + "% of the variation in the dependent variable \
can be explained by variation in the independent variables")

    p = f_test(predicted, y, n_vars)
    print("p-value (chance that model is equal to null): "+str(p))
    
    
    sc = StandardScaler()
    x_matrix = pandas.DataFrame(sc.fit_transform(x_matrix), columns = x_matrix.columns)

    print("\nUsing Lasso regression with alpha = " + str(lasso_alpha) + ":")
    coefs, score, predicted = lasso(x_matrix, y, lasso_alpha)
    
    if score > best_score:
        best_score = score
        best_pred = predicted
        best_coefs = coefs
    
    print("Intercept: " + str(coefs[-1]))
    for i in range(len(coefs)-1):
        print("Coefficient for " + x_matrix.columns[i] + ": " + str(coefs[i]))
        
    print(str(int(score * 10000)/100) + "% of the variation in the dependent variable \
can be explained by variation in the independent variables")

    p = f_test(predicted, y, n_vars)
    print("p-value (chance that model is equal to null): "+str(p))
    

    print("\nUsing Ridge regression with alpha = " + str(ridge_alpha) + ":")
    coefs, score, predicted = ridge(x_matrix, y, ridge_alpha)
    
    if score > best_score:
        best_score = score
        best_pred = predicted
        best_coefs = coefs
        
    if "output" in [s.lower().replace("-", "") for s in sys.argv]:
        outp = pandas.DataFrame(columns = ["Name", "Coefficient", "Mean", "Deviation", "ONEHOT"])
        outp["Name"] = data_sans_time.columns
        outp["ONEHOT"] = [name.startswith("ONEHOT") for name in outp["Name"]]
        outp.set_index("Name")
        outp.loc[0, "Coefficient"] = 0
        outp.loc[0, "Mean"] = best_coefs[-1]
        outp.loc[0, "Deviation"] = data_sans_time["Average Turbidity"].std()
        for i in range(len(x_matrix.columns)):
            col = x_matrix.columns[i]
            outp.loc[i + 1, "Coefficient"] = (col.replace(" ", ".").lower() != "average.turbidity") * best_coefs[i]
            outp.loc[i + 1, "Mean"] = x_matrix[col].mean()
            outp.loc[i + 1, "Deviation"] = x_matrix[col].std()
        
        outp.to_csv(files[0][:len(files[0]) - 4] + "_linreg.txt", sep = "\t", index = None)

    
    print("Intercept: " + str(coefs[-1]))
    for i in range(len(coefs)-1):
        print("Coefficient for " + x_matrix.columns[i] + ": " + str(coefs[i]))
        
    print(str(int(score * 10000)/100) + "% of the variation in the dependent variable \
can be explained by variation in the independent variables")

    p = f_test(predicted, y, n_vars)
    print("p-value (chance that model is equal to null): "+str(p))
    
    data["Predicted Turbidity"] = best_pred
    
    plt.plot("Average Turbidity", data = data, marker = "o", color = "black", linewidth = 2)
    plt.plot("Predicted Turbidity", data = data, marker = "o", color = "red", linewidth = 2)
    plt.legend(loc='upper right')
    plt.show()

main()