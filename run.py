import os, sys
from dijkstra import Graph

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

def printResult(dist):
    print(len(dist), sum(dist))

# Run all algoritms
graph = Graph(nodeCount, C, inputGraphList)
printResult(graph.dijkstra(0))
printResult(graph.dijkstra_radix(0))
printResult(graph.dijkstra_radix(0, level='Two level'))
printResult(graph.dijkstra_radix(0, level='Two level + Fibonacci Heap'))