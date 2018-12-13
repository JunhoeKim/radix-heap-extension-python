import os, sys
from dijkstra import Graph

nodeDic = {}

# Sample data used on http://www.dis.uniroma1.it/challenge9/download.shtml
# input file format also follows origin file format.
for line in open(sys.argv[1]):
    line = line.strip()
    if line.startswith("a"):
        command, parentNode, childNode, distance = line.split()
        
        parentNode = int(parentNode)
        childNode = int(childNode)
        distance = int(distance)
        nodeDic.setdefault(parentNode, []).append((childNode, distance))
    else:
        continue

inputGraphList = []
for key in range(max(nodeDic.keys())+1):
    inputGraphList.append(nodeDic.setdefault(key, []))    


print(inputGraphList[:5])
print(inputGraphList[-5:])

graph = Graph(inputGraphList)
graph.dijkstra(0)
graph.dijkstra_radix(0)
graph.dijkstra_radix(0, level='Two level')
graph.dijkstra_radix(0, level='Two level + Fibonacci Heap')