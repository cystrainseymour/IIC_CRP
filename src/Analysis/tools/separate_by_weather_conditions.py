import sys
import os

def separate(data, col, cutoff):
    #print(data, col, cutoff)
    data1 = []
    data2 = []
    
    for row in data:
        #print(row)
        if row[col] <= cutoff:
            data1.append(row)
        else:
            data2.append(row)
    
    return data1, data2
    
def format_data(data):
    return "\n".join(["\t".join(list(map(str,row))) for row in data])

def main():
    path = sys.argv[1]
    inp = open(path, "r")
    arg = sys.argv[2].lower().replace(" ", "_")
    cutoff = 0.0
    try:
        cutoff = sys.argv[3]
    except:
        pass
    
    vars_orig = inp.readline().strip().split("\t")
    vars = list(map(lambda s:s.lower().replace(" ", "_"),vars_orig))
    n_vars = len(vars)
    
    data = []
    n = 0
    while True:
        try:
            line = inp.readline().strip().split("\t")
            if len(line) == 1:
                break
            data.append([])
            for i in range(n_vars):
                entry = line[i]
                try:
                    entry = float(entry)
                except:
                    pass
                data[n].append(entry)
            n += 1
        except IndexError:
            break
        except EOFError:
            break
    
    try:
        col = [i for i in range(n_vars) if vars[i] == arg][0]
    except:
        raise ValueError
    
    data1, data2 = separate(data,col,cutoff)
    
    base = path.split("/")
    file = base[-1].split(".")[-2]
    base = base [:len(base)-1]
    
    folder = "/".join(base + ["_".join([file,"split_by",arg])])
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(folder + "//lte_" + str(cutoff) + ".txt", "w") as outp:
        outp.write("\t".join(vars_orig))
        outp.write("\n")
        outp.write(format_data(data1))
    with open(folder + "//gt_" + str(cutoff) + ".txt", "w") as outp:
        outp.write("\t".join(vars_orig))
        outp.write("\n")
        outp.write(format_data(data2))
        
if __name__ == "__main__":
    main()