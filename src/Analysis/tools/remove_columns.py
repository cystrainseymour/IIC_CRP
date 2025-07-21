import sys
import pandas

def remove_cols(df, cols):
    for col in cols:
        try:
            df.drop(col, axis = 1, inplace = True)
        except KeyError:
            print(col, "not found in the data")
        
    
def main():
    inp = sys.argv[1]
    outp = sys.argv[2]
    cols = sys.argv[3:]
    
    data = pandas.read_csv(inp, sep = "\t")
    remove_cols(data, cols)
    
    data.to_csv(outp, sep = "\t", index = None)
    
if __name__ == "__main__":
    main()