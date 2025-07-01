import sys

def main():
    with open(sys.argv[1], "r") as inp:
        args = map(lamba s: s.lower(), sys.argv[2:])
        vars = inp.readline().strip().split("\t")
        print(vars)
        which = []
        for arg in args:
            found = False
            for i in range(len(vars)):
                if arg == vars[i]:
                    which.append(i)
                    found = True
                    break
            if not found:
                print(arg + " not found in file")
        if not len(which):
            sys.exit()
        data = []
        try:
            while True:
                line = inp.readline().strip().split("\t")
                for i in range(len(which)):
                        try:
                            data[i].append(line[which[i]]) 
                        except IndexError:
                            data.append([])
                            data[i].append(line[which[i]])
        except:
            for i in range(len(which)):
                print(vars[which[i]])
                for j in range(len(data[i])):
                    print(data[i][j])
                print("\n")
                
main()