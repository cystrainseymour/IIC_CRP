import sys
import math

def read_data(inp, col = 0):
    data = []
    
    for file in inp:
        f = open(file, "r")
        while True:
            try:
                entry = f.readline().split("\t")[col]
                
                if entry.isalpha():
                    continue
                data.append(float(entry))
            except Exception as e:
                
                break
    
    return data    
    
def mean(data):
    return sum(data)/len(data)
    
def standard_deviation(data, ave = None):
    if ave is None:
        ave = mean(data)
    total = sum([math.pow(i - ave, 2) for i in data])
    return math.sqrt(total/(len(data)-1))
    
def get_t_score(value, ave, dev, ratio = 1):
    return ratio*(value - ave)/(dev)
    
def main():
    ratio = 1
    offset = 0
    if sys.argv[-1].isnumeric():
        ratio = float(sys.argv[-1])
        offset = 1
    
    inp = sys.argv[1:len(sys.argv) - 2 - offset]
    col = int(sys.argv[-2 - offset])
    if not len(inp):
        inp = sys.argv[1:len(sys.argv) - 1 - offset]
        col = 0
    outp = sys.argv[-1 - offset]
    
    data = read_data(inp, col)
    
    ave = mean(data)
    dev = standard_deviation(data, ave)
    minim = min(data)
    maxim = max(data)
    
    range_units = maxim-minim
    std_bel = int(abs(get_t_score(minim, ave, dev))+1)
    std_abo = int(get_t_score(maxim, ave, dev)+1)
    range_std = std_bel + std_abo
    #print(std_bel, std_abo)
    
    buckets = [0 for i in range(int(range_std * ratio))]
    
    for i in data:
        t = int((get_t_score(i, ave, dev) + std_bel) * ratio)
        #print(i, t)
        buckets[t] += 1
        
    #print(buckets)
        
    print("Mean:", ave)
    print("Standard Deviation:", dev)
    print("Range:", range_units, "("+str(range_std),"standard deviations)")
    print("Buckets:")
    for i in range(int(std_bel * ratio)):
        print(str((i - std_bel * ratio)/ratio) + " " + str(buckets[i]))
    for i in range(int(std_bel * ratio), int(range_std * ratio)):
        print(str((i - std_bel * ratio)/ratio) + " " + str(buckets[i]))
    
    with open(outp, "w") as f:
        f.write(" ".join(list(map(str,[ave, dev, range_units, range_std]))))
        f.write("\n")
        f.write("\n".join(list(map(str,buckets))))
    
if __name__ == "__main__":
    main()