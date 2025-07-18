import sys
from datetime import datetime
import pandas as pd

def parse_date(row, time_col):
    date = row[time_col]
    try:
        date = datetime.strptime(date, "%B %d, %Y %I:%M %p")
    except ValueError:
        try:
            date = datetime.strptime(date, "%I:%M %p, %B %d")
        except ValueError:
            try:
                date = datetime.strptime(date, "%Y/%m/%d %I:%M %p")
            except ValueError:
                try:
                    date = datetime.strptime(date, "%Y/%m/%dT%I:%M %p")
                except ValueError:
                    date = datetime.strptime(date, "%Y/%m/%d, %I:%M %p")
                    
    return date

def add_one_hot(df, time_col = None):
    if time_col is None:
        for name in df.columns:
            if "time" in name.lower() or "temps" in name.lower():
                time_col = name
                break
                
        if time_col is None:
            for name in df.columns:
                if "date" in name.lower():
                    time_col = name
                    break
                
            if time_col is None:
                print("Please call the time column \"time\" or \"date\"")
                raise ValueError
    
    dates = df.apply(lambda r: parse_date(r, df.columns.get_loc(time_col)), axis = 1)
    
    hours = [[0 for j in range(len(df.index))] for i in range(24)]
    for i in range(len(df.index)):
        hours[dates[i].hour][i] = 1
    
    for i in range(24):
        df["ONEHOT_Hour"+str(i+1)] = hours[i]

def main():
    inp = sys.argv[1]
    outp = sys.argv[2]
    
    data = pd.read_csv(inp, sep="\t")
    
    add_one_hot(data)
    print(data.head())
    
    data.to_csv(outp, sep = "\t", index = False)
    
if __name__ == "__main__":
    main()