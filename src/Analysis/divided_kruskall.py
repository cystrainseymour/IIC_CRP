import sys
import os
import warnings
import math
import re
from scipy.stats import kruskal

'''
    Given data from two or more different samples (e.g. one stream from a restored area and one
    from a non-restored area, or two samples of the same stream before and after restoration),
    and optionally different weather conditions, this program will split each sample into groups 
    based on the conditions (e.g. high-rain and low-rain groups) and then perform the Kruskal-Wallace
    H-test on each group between the samples (e.g. comparing low-rain from Sample A with low-rain from
    Sample B), and then for each group, it returns the probability that both come from the same 
    distribution. A low p-value/probability means it's less likely the difference is due to chance,
    and a higher probability there is something actually different between the sites the samples
    came from.
    
    divided_kruskal() can be called on its own from another file, but the program can also be run from
    the command line. To do this, use the format: 
    
    py is_difference_significant.py [1st/file.txt] [2nd/file.txt] ... (--normalize) var1 val1 var2 val2 ...
    
    For example:
    
    py is_difference_significant.py "../../data/Tinkling Rill (6_17 - 6_23)/comp.txt" 
    "../../data/Chickahominy (6_6 - 6_7)/comp.txt"  "10min_rainfall 0"
    
    Adding "normalize" or "--normalize" after the files but before the conditions will normalize the 
    turbidity data. Adding no conditions will have the program perform the test on all the data from 
    all the samples together.    
    
    For specifying weather conditions, the following formats all do the same thing: "variable value",
    "variable=value", "variable<=value", "variable<value", "variable-value". The variable names aren't
    case-sensitive, and spaces, periods, and underscores are interchangeable.
    
    Data should be in a tab-separated values format.
'''

# rescale data so that it falls within the range 0-1
# useful for when the sensors haven't been calibrated, 
# but it's probably more robust without normalization 
def normalize(data):
    maxim = 0
    minim = -1
    for datum in data:
        if datum > maxim:
            maxim = datum
        elif datum < minim or minim == -1:
            minim = datum
    data_range = maxim - minim
    if not data_range:
        data = [0.5]*len(data)
        return
    for i in range(len(data)):
        data[i] -= minim
        data[i] /= data_range
    
# given the titles of the variables in different samples,
# return only the titles/variables that are common between 
# all of the samples (after adjusting for formatting)
def get_common_variables(*args):
    union = []
    n_union = []
    for arg in args:
        for title in arg:
            title = re.sub(" |-|\\.","_",title.strip().lower())
            found = False
            for i in range(len(union)):
                if union[i] == title:
                    n_union[i] += 1
                    found = True
                    break
            if not found:
                union.append(title)
                n_union.append(1)
    
    return [union[i] for i in range(len(union)) if n_union[i] == len(args)]
    
# given the titles of the columns and the cutoffs for each 
# variable, return the list of the cutoff values in the order 
# that the corresponding columns appear -- with None in the 
# spots that correspond to columns without specified cutoff values
def initialize_cutoffs(titles, **kwargs):
    n_vars = len(titles)
    cutoffs = [None]*(n_vars)
    
    names = list(kwargs.keys())
    values = list(kwargs.values())
    
    for i in range(len(names)):
        name = names[i].strip().lower().replace(" ","_")
        found = False
        for j in range(n_vars):
            title = titles[j].strip().lower().replace(" ","_")
            
            if title == name:
                cutoffs[j] = values[i]
                found = True
                break
        if not found:
            warnings.warn(names[i] + " not found in list of variables")
    #print(cutoffs)
    return cutoffs

# divide data into an arbitrary number of groups using cutoffs
def divide(data, cutoffs, titles):
    groups = [[]]
    cols = []
    
    n = len(data)
    for i in range(len(cutoffs)):
        if not cutoffs[i] is None:
            groups.append([]*len(groups))
            cols.append(i)

    n_vars = len(cols)
    if len(groups) == 1:
        return [data[1:]], []

    divisions = [[] for i in range(len(groups))]
    for c in range(n_vars):
        for i in range(0,int(len(groups)/2),int(math.pow(2,c))):
            for j in range(int(math.pow(2,c))):
                divisions[i+j].append("".join(titles[cols[c]] + "<=" + str(cutoffs[cols[c]])))

    for c in range(n_vars):
        for i in range(int(len(groups)/2),0,-1*int(math.pow(2,c+1))):
            for j in range(int(math.pow(2,c))):
                divisions[i+j].append("".join(titles[cols[c]] + ">" + str(cutoffs[cols[c]])))
    
    for r in range(1,n):
        g = [False]*len(groups)
        for c in range(n_vars):
            if data[r][cols[c]] <= cutoffs[cols[c]]:
                for i in range(0,int(len(groups)/2),int(math.pow(2,c))):
                    for j in range(int(math.pow(2,c))):
                        g[i+j] = True
            else:
                for i in range(int(len(groups)/2),0,int(-1*math.pow(2,c+1))):
                    for j in range(int(math.pow(2,c))):
                        g[i+j] = True
        for i in range(len(g)):
            if g[i]:
                groups[i].append(data[r])

    return (groups, divisions)

# perform Kruskal-Wallace H-test on each group across the different samples
def h_test(sample_groups):
    g = len(sample_groups)
    k = len(sample_groups[0])
    results = []*k
    for group in range(k): # for each weather-based group in each sample (taken in different times/places)
        group_data = []
        for sample in range(g): # get the data for that group in each sample
            group_data.append(sample_groups[sample][group])
        h, p = kruskal(*[sample_groups[sample][group] for sample in range(g)])
        results.append(p)
    return results
    
# "main" part - given the samples and cutoff keywords, 
# find the common variables, divide each sample into groups,
# and perform the H-test on each. Return the p-values for each
# group, as well as the divisions/labels for which corresponds 
# to which group. Can be run/called independently
def divided_kruskal(normal = False, *samples, **kwargs):
    
    lines = []
    for sample in samples:
        lines.append(sample[0])
    titles = get_common_variables(*lines)
    
    
    sample_groups = []
    all_divisions = []
    for sample in samples:
        cutoffs = initialize_cutoffs(titles, **kwargs)
        line = sample[0]

        turbid_col = 1        
        for i in range(len(line)):
            title = re.sub(" |-|\\.","_",line[i].strip().lower())
            if "turbid" in title:
                turbid_col = i

        groups, divisions = divide(sample, cutoffs, line)

        groups_turbidity = []
        all_divisions.append(divisions)
        for group in groups:
            #print(group)
            if len(group):
                turbidity = [row[turbid_col] for row in group]
                if normal:
                    normalize(turbidity)
                groups_turbidity.append(turbidity)
            else:
                groups_turbidity.append([])
        sample_groups.append(groups_turbidity)
        
    results = h_test(sample_groups)
    
    return results, all_divisions[0]
    
# part of the user-interface - given strings from 
# the command line corresponding to the conditions,
# return them in a dictionary
def get_cutoffs_dict(strings):
    names_values = list(map(lambda s : re.split(" |=|-|<=|<",s), strings))
    names = [name[0] for name in names_values]
    values = [float(name[1]) for name in names_values]
    
    cutoffs = {}
    for i in range(len(names)):
        cutoffs[names[i]] = float(values[i])

    return cutoffs

# for the user-interface/command line - read in
# the files provided by the command line, check if
# the "normalize" keyword is used, and get the conditions.
# Format the conditions in a dictionary, and pass the data,
# conditions, and whether or not to normalize to kruskal_wallace.
# Format and print the results in a readable way
def main():
    files = []
    
    count = 1
    while count < len(sys.argv) and os.path.exists(sys.argv[count]):
        files.append(sys.argv[count])
        count += 1
    
    if count < 2:
        print("Please provide at least two files of tab-separated values")
        raise ValueError
       
    normalize = False
    if sys.argv[count].strip("-").lower() == "normalize":
        normalize = True
        count += 1
    
    cutoff_kwargs = get_cutoffs_dict(sys.argv[count:])
    
    samples = []
    for file in files:
        data = []
        print("Reading from:", file)
        inp = open(file, "r")
        for line in inp:
            l = line.strip().split("\t")
            for i in range(len(line)):
                try:
                    l[i] = float(l[i])
                except:
                    pass
            data.append(l)
        print(len(data), " lines read in\n")
        inp.close()
        samples.append(data)

    results, divisions = divided_kruskal(normalize, *samples, **cutoff_kwargs)
    
    print("\nUsing the Kruskal-Wallace test:")
    
    if not len(divisions):
        print("\tp-value (chance that the data from the different samples are from the same distribution):",\
        results[0])
    else:
        for i in range(len(divisions)):
            print("\tFor the sections of the samples fulfilling the following conditions:")
            for condition in divisions[i]:
                print("\t\t-\t" + condition)
            print("\tp-value (chance that the data from the different samples are from the same distribution):",\
            results[i])
            print("\n")
    
    
    
if __name__ == "__main__":
    main()