import sys
import os
import random

def is_before_or_at(date1, date2):
    date1[3] += 12 * date1[5]
    date2[3] += 12 * date2[5]
    for i in range(5):
        if date2[i] > date1[i]:
            date1[3] -= 12 * date1[5]
            date2[3] -= 12 * date2[5]
            return True
        elif date2[i] < date1[i]:
            date1[3] -= 12 * date1[5]
            date2[3] -= 12 * date2[5]
            return False
    return date1[4] == date2[4] 
    
def get_next_date(date):
    new = []
    for i in date:
        new.append(i)
    if new[4] >= 50:
        new[4] = (new[4] + 10) % 60
        new[3] = (new[3] + 1) % 13
        if not new[3]:
            new[3] = 12
            if new[5]:
                if new[2] == 30:
                    new[2] = 0
                    if new[1] == 12:
                        new[1] = 0
                        new[0] += 1
                    new[1] += 1
                new[2] += 1
            new[5] = not new[5]
    else:
        new[4] += 10
    return new
    
def add_a_week(date):
    new = []
    for i in date:
        new.append(i)
    new[2] = (new[2] + 7) % 31
    new[2] += not new[2]
    if new[2] < date[2]:
        new[1] = (new[1] + 1) % 13
        new[1] += not new[1]
        if new[1] < date[1]:
            new[0] += 1
    return new

def main():
    path = "test_data"
    n = []
    cols = ["Datetime", "Average.Turbidity"]
    corrs = [0, 0]
    
    i = 1
    while i < len(sys.argv):
        p = sys.argv[i].split("/")
        if os.path.exists("/".join(p[:len(p) - 1])):
            path = sys.argv[i]
        elif "treat" == sys.argv[i].lower() or "treat" in sys.argv[i].lower():
            i += 1
            corrs[1] = float(sys.argv[i])
        elif not sys.argv[i].isdigit():
            cols.append(sys.argv[i])
            i += 1
            corrs.append(float(sys.argv[i]))
        else:
            n.append(int(sys.argv[i]))
        i += 1
    
    if not len(n):
        n = [2,9]

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    dates = [[2025, 6, 1, 3, 50, True]]
    for i in range(n[0] - 1):
        new = get_next_date(dates[i])
        dates.append(new)
    
    starts = [[2025, 5, 30, 4, 00, False], 300, 0.5, 60]
    devs = [0, 50, 1, 20]
    end_date = add_a_week(dates[-1])
        
    treated = []
    for i in range(n[0]):
        sample = []
        sample.append(["\t".join(cols)])
        date = starts[0]
        
        while is_before_or_at(date, dates[i]):
            row = []
            date = get_next_date(date)
            if date[5]:
                row.append(months[date[1] - 1] + " " + str(date[2]) + ", " + str(date[0]) + " " + str(date[3]) + ":" + str(date[4]).zfill(2) + " PM")
            else:
                row.append(months[date[1] - 1] + " " + str(date[2]) + ", " + str(date[0]) + " " + str(date[3]) + ":" + str(date[4]).zfill(2) + " AM")
            
            vals = []
            
            for j in range(2,len(cols)):
                maxim = starts[j] + devs[j]
                minim = starts[j] - devs[j]
                
                vals.append(max(0,random.random()*maxim + minim))
                
            maxim = starts[1] + devs[1]
            minim = starts[1] - devs[1]
            
            for j in range(2,len(cols)):
                maxim += vals[j-2] * corrs[j]
                minim += vals[j-2] * corrs[j]
            
            row.append(max(0,random.random()*maxim + minim))
            for val in vals:
                row.append(val)
                
            sample.append(row)
        
        while is_before_or_at(date, end_date):
            row = []
            date = get_next_date(date)
            if date[5]:
                row.append(months[date[1] - 1] + " " + str(date[2]) + ", " + str(date[0]) + " " + str(date[3]) + ":" + str(date[4]).zfill(2) + " PM")
            else:
                row.append(months[date[1] - 1] + " " + str(date[2]) + ", " + str(date[0]) + " " + str(date[3]) + ":" + str(date[4]).zfill(2) + " AM")
            
            vals = []
            
            for j in range(2,len(cols)):
                maxim = starts[j] + devs[j]
                minim = starts[j] - devs[j]
                
                vals.append(max(0,random.random()*maxim + minim))
                
            maxim = starts[1] + devs[1]
            minim = starts[1] - devs[1]
            
            for j in range(2,len(cols)):
                maxim += vals[j-2] * corrs[j]
                minim += vals[j-2] * corrs[j]
                
            maxim += maxim * corrs[1]
            minim += minim * corrs[1]
            
            row.append(max(0,random.random()*maxim + minim))
            for val in vals:
                row.append(val)
            
            sample.append(row)
            
        treated.append(sample)
        
    untreated = []
    for i in range(n[1]):
        sample = []
        sample.append(cols)
        date = starts[0]
        
        while is_before_or_at(date, end_date):
            row = []
            date = get_next_date(date)
            if date[5]:
                row.append(months[date[1] - 1] + " " + str(date[2]) + ", " + str(date[0]) + " " + str(date[3]) + ":" + str(date[4]).zfill(2) + " PM")
            else:
                row.append(months[date[1] - 1] + " " + str(date[2]) + ", " + str(date[0]) + " " + str(date[3]) + ":" + str(date[4]).zfill(2) + " AM")
            
            vals = []
            
            for j in range(2,len(cols)):
                maxim = starts[j] + devs[j]
                minim = starts[j] - devs[j]
                
                vals.append(max(0,random.random()*maxim + minim))
                
            maxim = starts[1] + devs[1]
            minim = starts[1] - devs[1]
            
            for j in range(2,len(cols)):
                maxim += vals[j-2] * corrs[j]
                minim += vals[j-2] * corrs[j]
            
            row.append(max(0,random.random()*maxim + minim))
            for val in vals:
                row.append(val)
                
            sample.append(row)
            
        untreated.append(sample)
    
    base = path + "/" + "treated"
    os.makedirs(base)
    for i in range(len(treated)):
        file = base + "/" + "file_" + str(i+1) + ".txt"
        with open(file, "w") as outp:
            for r in treated[i]:
                outp.write("\t".join(list(map(str,r))) + "\n")
    
    base = path + "/" + "untreated"
    os.makedirs(base)
    for i in range(len(untreated)):
        file = base + "/" + "file_" + str(i+1) + ".txt"
        with open(file, "w") as outp:
            for r in untreated[i]:
                outp.write("\t".join(list(map(str,r))) + "\n")
    
    dates_str = [months[date[1] - 1] + " " + str(date[2]) + ", " + str(date[0]) + " " + str(date[3]) + ":" + str(date[4]).zfill(2) + " PM" if date[5] else months[date[1]] + " " + str(date[2]) + ", " + str(date[0]) + " " + str(date[3]) + ":" + str(date[4]).zfill(2) + " AM" for date in dates]
    print(dates_str)
    
if __name__ == "__main__":
    main()