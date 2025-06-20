import sys

def is_before(date1, date2):
    for i in range(2):
        for j in range(4):
            if date1[i][j] < date2[i][j]:
                return True
    return False

def is_equal(date1, date2):
    for i in range(2):
        for j in range(4):
            if date1[i][j] != date2[i][j]:
                return False
    return True
    
def find_relevant_entries(line, entries):
    to_r = []
    for i in range(len(line)):
        if entries[i]:
            to_r.append(line[i])
    return to_r

def find_relevant_rows(inp, begin, end, entries):
    line = list(map(lambda s: s.strip("\""), inp.readline().split(",")))
    date = line[1].strip("\"").split("T")
    date = [list(map(int,date[0].split("-"))),list(map(int,date[1].split(":")))]
    
    while is_before(date, begin):
        line = list(map(str.strip, inp.readline().split(",")))
        try:
            date = line[1].strip("\"").split("T")
            date = [list(map(int,date[0].split("-"))), list(map(int,date[1].split(":")))]
        except IndexError:
            return []
    
    rows = []
    rows.append(find_relevant_entries(line, entries))
    
    while is_before(date, end) or is_equal(date, end):
        line = list(map(lambda s: s.strip("\""), inp.readline().split(",")))
        date = line[1].split("T")
        date = [date[0].split("-"),date[1].split(":")]
        rows.append(find_relevant_entries(line, entries))
    
    return rows
    
def main():
    args = sys.argv[1:]
    if len(args) < 13:
        args = input("Incorrect number of arguments. Please try again: ").split()
    inp = open(args[0], "r")
    
    begin_date = list(map(int,args[2:5]))
    begin_time = list(map(int,args[5:7]))
    begin_time.append([0])
    begin = [begin_date,begin_time]
    
    end_date = list(map(int,args[7:10]))
    end_time = list(map(int,args[10:12]))
    end_time.append([0])
    end = [end_date,end_time]
    
    vars = list(map(lambda s: s.strip("\""), inp.readline().split(",")))
    print(vars)
    entries = []
    for i in range(len(vars)):
        if vars[i] in args:
            entries.append(True)
        else:
            entries.append(False)
    
    entries[1] = True
    
    rel_rows = find_relevant_rows(inp, begin, end, entries)
    
    with open(args[1], "w") as outp:
        for i in range(len(entries)):
            if entries[i]:
                outp.write(vars[i] + "\t")
        outp.write("\n")
        
        for i in rel_rows:
            outp.write("\t".join(i))
            outp.write("\n")
            
main()