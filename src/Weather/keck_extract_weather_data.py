import sys
import os

def is_before(date1, date2):
    for i in range(5):
        if date1[i] < date2[i]:
            return True
    return False

def is_equal(date1, date2):
    for i in range(5):
        if date1[i] != date2[i]:
            return False
    return True
    
def extract_date(d, t):
    date = list(map(int,d.split("/")))
    #print(d, date)
    if len(date) < 3:
        date = list(map(int,d.split("-")))
    date[2] %= 2000
    
    time_pre = t.split()
    time = list(map(int,time_pre[0].split(":")))
    if time[0] != 12 and time_pre[-1].lower().startswith("p"):
        time[0] += 12
    elif time[0] == 12 and not time_pre[-1].lower().startswith("p"):
        time[0] = 0
    
    return [date[2], date[0], date[1], time[0], time[1]]
    
def extract_col_names(line1, line2):
    l1 = list(map(lambda s:s.strip(), line1.split("\t")))
    l2 = list(map(lambda s:s.strip(), line2.split("\t")))
    return [".".join([l1[i], l2[i]]).strip(".") for i in range(len(l1))]
    
def find_relevant_entries(line, entries):
    to_r = []
    for i in range(len(line)):
        if entries[i]:
            to_r.append(line[i])
    return to_r

def find_relevant_rows(inp, begin, end, entries):
    line = inp.readline().split("\t")
    
    date = extract_date(line[0], line[1])
    
    while is_before(date, begin):
        line = inp.readline().split("\t")
        try:
            date = extract_date(line[0], line[1])
        except IndexError:
            print("Nothing found")
            return []
    
    rows = []
    rows.append(find_relevant_entries(line, entries))
    
    while is_before(date, end):
        try:
            line = inp.readline().split("\t")
            date = extract_date(line[0], line[1])
            rows.append(find_relevant_entries(line, entries))
        except:
            print("File ends at date ", "-".join(list(map(lambda i:str(i), date))))
            break
    
    return rows
    
def extract_date_str(date_str):
    begin_str = date_str.strip().split(" ")
    time = begin_str[0].split(":")
    
    time = list(map(int,begin_str[0].split(":")))
    
    if begin_str[1].lower().startswith("p") and time[0] != 12:
        time[0] += 12
    elif not begin_str[1].lower().startswith("p") and time[0] == 12:
        time[0] = 0
    
    calendar = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    
    date = [25] + [i+1 for i in range(len(calendar)) if calendar[i] == begin_str[2]] + [int(begin_str[3])]
    
    return date + time
    
def find_relevant_rows_given_times(dat_inp, tim_inp, entries):
    line = dat_inp.readline().split("\t")
    
    date = extract_date(line[0], line[1])
    
    tim_inp.readline()
    begin = extract_date_str(tim_inp.readline())
    
    while is_before(date, begin):
        line = dat_inp.readline().split("\t")
        try:
            date = extract_date(line[0], line[1])
        except IndexError:
            print("Nothing found")
            return []
    
    rows = []
    rows.append(find_relevant_entries(line, entries))
    cur = extract_date_str(tim_inp.readline())
    
    line = dat_inp.readline().split("\t")
    date = extract_date(line[0], line[1])
    print(date, cur)
    
    while True:
        try:
            if is_equal(cur, date):
                rows.append(find_relevant_entries(line, entries))
                cur = extract_date_str(tim_inp.readline())
            else:    
                line = dat_inp.readline().split("\t")
                date = extract_date(line[0], line[1])
                
            print(date, cur)
        except Exception as e:
            print(e)
            break
    
    return rows
    
def main():
    args = sys.argv[1:]
    if len(args) < 3:
        args = input("Incorrect number of arguments. Please try again").split()
        sys.exit()
    inp = open(args[0], "r")
    
    mode = "w"
    tim_inp = None
    start = 8
    if os.path.exists(args[2]):
        tim_inp = open(args[2],"r")
        start = 3
    else:
        begin = extract_date(args[2], " ".join([args[3], args[4]]))
        end = extract_date(args[5], " ".join([args[6], args[7]]))
    #print(begin, end)
    
    vars = extract_col_names(inp.readline(), inp.readline())
    #print(vars)
    entries = [False] * len(vars)
    for i in range(len(vars)):
        for j in range(start, len(args)):
            if j == len(args)-1 and args[j].lower() == "a":
                mode = "a"
                break
            if vars[i].lower().startswith(args[j].lower()):
                entries[i] = True
                break
    
    entries[0] = entries[1] = True # date and time always included
    #print(entries)
    rel_rows = []
    if tim_inp is None:
        rel_rows = find_relevant_rows(inp, begin, end, entries)
    else:
        rel_rows = find_relevant_rows_given_times(inp, tim_inp, entries)
    
    with open(args[1], mode) as outp:
        for i in range(len(entries)):
            if entries[i]:
                outp.write(vars[i] + "\t")
        outp.write("\n")
        
        for i in rel_rows:
            outp.write("\t".join(i))
            outp.write("\n")
            
main()