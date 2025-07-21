import sys
import pandas as pd
import numpy as np

def remove_outliers(data, cols):
    beg = 0
    end = 0
    for col in cols:
        med = data[col].median()
        iqr = np.quantile(data[col], 0.75) - np.quantile(data[col], 0.25)
        
        iqr *= 1.5
        minim = med - iqr
        maxim = med + iqr
        
        beg += len(data[data[col] < med - iqr])
        end += len(data[data[col] > med + iqr])
        
        data.drop(data[data[col] < med - iqr].index, axis = 0, inplace = True)
        data.drop(data[data[col] > med + iqr].index, axis = 0, inplace = True)
        
    return beg, end

def main():
    
    inp = sys.argv[1]
    outp = sys.argv[2]
    
    data = pd.read_csv(inp, sep="\t")
    
    cols = [data.columns[1]]
    if len(sys.argv) >= 4:
        cols = sys.argv[3:]
    
    beg, end = remove_outliers(data, cols)
    print(beg, "left outliers and", end, "right outliers removed from data")
    
    data.to_csv(outp, sep = "\t", index = False)
    
if __name__ == "__main__":
    main()