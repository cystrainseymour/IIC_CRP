import sys

def main():
    outp = None
    if sys.argv[2] == "-w":
        outp = sys.argv[3]
    with open(sys.argv[1], "r") as inp:
        args = list(map(lambda s: s.lower(), sys.argv[2:]))
        if not outp is None:
            args = list(map(lambda s: s.lower(), sys.argv[4:]))
        vars = list(map(lambda s: s.lower(), inp.readline().strip().split("\t")))
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
            return
        data = []
        
        
        try:
            while True:
                line = inp.readline().strip().split("\t")
                to_r = []
                for i in range(len(which)):
                    to_r.append(line[which[i]])
                data.append("\t".join(to_r))
        except:
            if not outp is None:
                with open(outp, "w") as f:
                    f.write("\t".join(sys.argv[4:]))
                    f.write("\n")
                    for i in data:
                        f.write(i)
                        f.write("\n")
                return
            print("\t".join(sys.argv[2:]))
            for i in data:
                print(data)
                
if __name__ == "__main__":
    main()