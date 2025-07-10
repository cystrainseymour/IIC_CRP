import sys

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

def remove_outliers(data):
    data.sort()
    n = len(data)
    
    med = data[int(n/2)]
    q1 = data[int(n/4)]
    q3 = data[int(3*n/4)]
    if (not n % 2):
        med += data[int(1 + n/2)]
        med /= 2
        q1 = data[int(n/4)]
        q3 = data[int(3*n/4)]
        if (not n % 4):
            q1 += data[int(n/4) + 1]
            q3 += data[int(3*n/4) + 1]
            q1 /= 2
            q3 /= 2
    elif not (n-1) % 4:
        q1 += data[int(n/4) + 1]
        q3 += data[int(3*n/4) + 1]
        q1 /= 2
        q3 /= 2
        
    iqr = abs(q3-q1)
    
    iqr *= 1.5
    minim = med - iqr
    maxim = med + iqr
    #print(n, med, q1, q3, iqr, minim, maxim)
    
    start = 0
    while data[start] < minim:
        start += 1
    
    end = n - 1
    while data[end] > maxim:
        end -= 1
        
    data = data[start:end+1]
    return start, n - end - 1

def main():
    
    inp = sys.argv[1:len(sys.argv)-2]
    col = int(sys.argv[-2])
    if not len(inp):
        inp = sys.argv[1:len(sys.argv)-1]
        col = 0
    data = read_data(inp, col)
    
    outp = sys.argv[-1]
    
    beg, end = remove_outliers(data)
    print(beg, "left outliers and", end, "right outliers removed from data")
    
    with open(outp, "w") as f:
        f.write("\n".join(list(map(str,map(int,data)))))
        
if __name__ == "__main__":
    main()