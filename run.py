import os, sys
from dijkstra import Graph
import datetime

nodeDic = {}
nodeCount = 0
C = 0
# Sample data used on http://www.dis.uniroma1.it/challenge9/download.shtml
# input file format also follows origin file format.
# ex) a 1 2 803
for line in open(sys.argv[1]):
    line = line.strip()
    if line.startswith("a"):
        command, parentNode, childNode, distance = line.split()
        
        parentNode = int(parentNode) - 1
        childNode = int(childNode) - 1
        distance = int(distance)
        if C < distance:
            C = distance

        # save data in dictionary
        nodeDic.setdefault(parentNode, []).append((childNode, distance))
    else:
        continue

# convert dictionary to graph list
inputGraphList = []
nodeCount = max(nodeDic.keys()) + 1
for key in range(nodeCount):
    inputGraphList.append(nodeDic.setdefault(key, []))    

# print(inputGraphList[:5])
# print(inputGraphList[-5:])

def printResult(str, start_time, dist):
    print("---------------------------")
    print(str)
    print(len(dist), sum(dist))
    print( int((datetime.datetime.now() - start_time).total_seconds() * 1000) / 1000.0 )
    print("---------------------------")
    
# Run all algoritms
graph = Graph(nodeCount, C, inputGraphList)
printResult("heapq", datetime.datetime.now(), graph.dijkstra(0))
printResult("naive heap", datetime.datetime.now(), graph.dijkstra_naive(0))
printResult("Radix level1", datetime.datetime.now(), graph.dijkstra_radix(0))
printResult("Radix level2", datetime.datetime.now(), graph.dijkstra_radix(0, level='Two level'))
printResult("Fib. Heap", datetime.datetime.now(), graph.dijkstra_radix(0, level='Two level + Fibonacci Heap'))