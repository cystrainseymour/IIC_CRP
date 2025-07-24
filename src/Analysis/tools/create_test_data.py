import sys
import os
import random
from datetime import datetime, timedelta
from scipy import stats
import pandas as pd

from one_hot import add_one_hot
from remove_outliers import remove_outliers
    
def get_next_date(date):
    delta = timedelta(hours = 1)
    return date + delta
    
def add_a_week(date):
    delta = timedelta(days = 7)
    return date + delta

def main():
    path = "test_data"
    inp = ""
    n = []
    cols = ["Datetime", "Average.Turbidity"]
    corrs = [0, 0]
    onehot_corrs = []
    
    starts = [datetime.strptime("2025/5/30 4:00 AM", "%Y/%m/%d %I:%M %p")]
    devs = [0]
    
    onehot = "onehot" in list(map(lambda s: s.lower().replace("_", ""), sys.argv))
    
    if os.path.exists(sys.argv[1]):
        data = pd.read_csv(sys.argv[1], sep = "\t")
        
        onehot_corrs = [corr for corr in data[[b for b in data["ONEHOT"]]]["Coefficient"]]
        
        data = data[[not b for b in data["ONEHOT"]]]
        cols += [name for name in data["Name"] if name != "Average Turbidity" and name != "Average.Turbidity"]
        corrs += [corr for corr in data["Coefficient"]]
        starts += [mean for mean in data["Mean"]]
        devs += [dev for dev in data["Deviation"]]
    
    #print(cols, corrs, starts, devs, onehot_corrs)
    
    if not len(n):
        n = [2,9]

    dates = [datetime.strptime("2025/6/1 3:00 PM", "%Y/%m/%d %I:%M %p")]
    for i in range(n[0] - 1):
        new = get_next_date(dates[i])
        dates.append(new)
    end_date = add_a_week(dates[-1])
    treatment_effect = 2
        
    samples = []
    
    for i in range(n[0]):
        sample = pd.DataFrame(columns = cols)
        sample["Datetime"] = [starts[0] + timedelta(hours = j) for j in range(int((dates[i] - starts[0]).days * 24 + (dates[i] - starts[0]).seconds/3600))]
        sample["Average.Turbidity"] = 0
        
        for j in range(2, len(cols)):
            dist = stats.foldnorm.rvs(c = 0, loc = starts[j], scale = devs[j], size = len(sample))
            
            sample[cols[j]] = dist
            sample["Average.Turbidity"] += corrs[j] * dist
        
        if onehot:
            add_one_hot(sample, "Datetime")
            for j in range(0, 24):
                dist = sample["ONEHOT_Hour" + str(j+1)]
                sample["Average.Turbidity"] += onehot_corrs[j] * dist
        
        #sample["Average.Turbidity"] += stats.foldnorm.rvs(c = 0, loc = starts[1] - (sum([corrs[j] * starts[j] for j in range(2, len(cols))]) + sum([onehot_corrs[j]/24 for j in range(24)])), scale = devs[0], size = len(sample))
        sample["Average.Turbidity"] += stats.foldnorm.rvs(c = 0, loc = starts[1], scale = devs[0], size = len(sample))
        sample["Treated"] = False
        
        post = pd.DataFrame(columns = cols)
        post["Datetime"] = [dates[i] + timedelta(hours = j) for j in range(int((end_date - dates[i]).days * 24 + (end_date - dates[i]).seconds/3600))]
        post["Average.Turbidity"] = 0
        
        for j in range(2, len(cols)):
            dist = stats.foldnorm.rvs(c = 0, loc = starts[j], scale = devs[j], size = len(post))
            
            post[cols[j]] = dist
            post["Average.Turbidity"] += corrs[j] * dist
        
        if onehot:
            add_one_hot(post, "Datetime")
            for j in range(0, 24):
                dist = post["ONEHOT_Hour" + str(j+1)]
                post["Average.Turbidity"] += onehot_corrs[j] * dist
        
        post["Average.Turbidity"] += [treatment_effect]*len(post)
        #post["Average.Turbidity"] += stats.foldnorm.rvs(c = 0, loc = starts[1] - sum([corrs[j] * starts[j] for j in range(2, len(cols))]) - sum([onehot_corrs[j]/24 for j in range(24)]), scale = devs[0], size = len(post))
        post["Average.Turbidity"] += stats.foldnorm.rvs(c = 0, loc = starts[1], scale = devs[0], size = len(post))
        post["Treated"] = True
        
        sample = pd.concat([sample, post])
        
        sample["Datetime"] = [datetime.strftime(date, "%B %d, %Y %I:%M %p") for date in sample["Datetime"]]
        
        remove_outliers(sample, ["Average.Turbidity"])
    
        samples.append(sample)
        
    for i in range(n[1]):
        sample = pd.DataFrame(columns = cols)
        sample["Datetime"] = [starts[0] + timedelta(hours = j) for j in range(int((end_date - starts[0]).days * 24 + (end_date - starts[0]).seconds/3600))]
        sample["Average.Turbidity"] = 0
        
        for j in range(2, len(cols)):
            dist = stats.foldnorm.rvs(c = 0, loc = starts[j], scale = devs[j], size = len(sample))
            
            sample[cols[j]] = dist
            sample["Average.Turbidity"] += corrs[j] * dist
        
        if onehot:
            add_one_hot(sample, "Datetime")
            for j in range(0, 24):
                dist = sample["ONEHOT_Hour" + str(j+1)]
                sample["Average.Turbidity"] += onehot_corrs[j] * dist
        
        #sample["Average.Turbidity"] += stats.foldnorm.rvs(c = 0, loc = starts[1] - sum([corrs[j] * starts[j] for j in range(2, len(cols))]) - sum([onehot_corrs[j]/24 for j in range(24)]), scale = devs[0], size = len(sample))
        sample["Average.Turbidity"] += stats.foldnorm.rvs(c = 0, loc = starts[1], scale = devs[0], size = len(sample))
        
        sample["Datetime"] = [datetime.strftime(date, "%B %d, %Y %I:%M %p") for date in sample["Datetime"]]
        
        remove_outliers(sample, ["Average.Turbidity"])
        
        sample["Treated"] = False
        
        samples.append(sample)
    
    os.makedirs(path)
    for i in range(len(samples)):
        file = path + "/" + "file_" + str(i+1) + ".txt"
        samples[i].to_csv(file, sep = "\t", index = None)
        
    dates_str = [datetime.strftime(i, "%B %d, %Y %I:%M %p") for i in dates]
    print(dates_str)
    
if __name__ == "__main__":
    main()