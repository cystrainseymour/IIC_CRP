import sys
import math

def distance(a,b):
    return math.sqrt(math.pow(a[0] - b[0],2) + math.pow(a[1] - b[1],2))
    
def compare_coords(target):
    file = open("C:/Users/cystr/Documents/Spring 2025/IIC_CRP/Weather/stations_list.txt", "r")
    min_dist = 1000
    arg_min_dist = ""
    try:
        count = 0
        while(True):
            line = file.readline().split()
            candidate = [float(line[1]), float(line[2])]
            dist = distance(target, candidate)
            if dist < min_dist:
                min_dist = dist
                arg_min_dist = " ".join(line)
            count+=1
    except IndexError as e:
        print("IndexError", e, count)
    except EOFError as e:
        print("EOFError", e, count)
    except Exception as e:
        print(e, count)
    return arg_min_dist
    
    
def main():
    target_lat = float(sys.argv[1])
    target_lon = float(sys.argv[2])
    print(compare_coords([target_lat, target_lon]))
    
main()