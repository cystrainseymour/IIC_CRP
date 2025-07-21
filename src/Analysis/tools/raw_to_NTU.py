import sys
import os
import pandas as pd

def drop_raw_cols(df):
    try:
        df.drop("+45", axis = 1, inplace = True)
        df.drop("+90", axis = 1, inplace = True)
        df.drop("-45", axis = 1, inplace = True)
        df.drop("-90", axis = 1, inplace = True)
    except:
        pass
    try:
        df.drop("Average.Turbidity", axis = 1, inplace = True)
    except:
        try:
            df.drop("Average Turbidity", axis = 1, inplace = True)
        except:
            pass
    try:
        df.drop("Raw", axis = 1, inplace = True)
    except:
        pass
    

def to_NTU(df, coef_45, coef_90, drop_raw = True):
    df["Turbidity (NTU)"] = (df["+45"] + df["-45"]) * coef_45 + (df["+90"] + df["-90"] * coef_90)
    if drop_raw:
        drop_raw_cols(df)

def main():
    inp = sys.argv[1]
    
    main_data = pd.read_csv(inp, sep="\t")
    
    coef_45 = 0
    coef_90 = 0
    data_path = ""
    drop_raw = False
    
    if len(sys.argv) <= 2:
        drop_raw_cols(main_data)
        main_data.to_csv(inp, sep = "\t", index = False)
        return
    
    for s in sys.argv[2:]:
        if os.path.exists(s):
            data_path = s
        elif "drop" in s.lower().replace("_", ""):
            drop_raw = True
        elif not coef_45:
            coef_45 = float(s)
        else:
            coef_90 = float(s)        
    
    if len(data_path):
        angles_data = pd.read_csv(data_path, sep="\t")
        main_data["+45"] = angles_data["+45"]
        main_data["-45"] = angles_data["-45"]
        main_data["+90"] = angles_data["+90"]
        main_data["-90"] = angles_data["-90"]
    
    if coef_45 or coef_90:
        to_NTU(main_data, coef_45, coef_90, drop_raw)
    
    main_data.to_csv(inp, sep = "\t", index = False)
    
if __name__ == "__main__":
    main()