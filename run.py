import os, sys
from dijkstra import Graph
from collections import defaultdict
import datetime

node_dict = defaultdict(lambda: [])
n = 0
C = 0
# Sample data used on http://www.dis.uniroma1.it/challenge9/download.shtml
# input file format also follows origin file format.
# ex) a 1 2 803
for line in open(sys.argv[1]):
    line = line.strip()
    if line.startswith("a"):
        command, parent_node, child_node, distance = line.split()
        
        parent_node = int(parent_node) - 1
        child_node = int(child_node) - 1
        distance = int(distance)
        if C < distance:
            C = distance

        # save data in dictionary
        node_dict[parent_node].append((child_node, distance))
    else:
        continue

# Convert dictionary to graph list
n = max(node_dict.keys()) + 1
adjacents = [x[1] for x in sorted(node_dict.items(), key=lambda x: x[0])]

def print_result(str, start_time, dist):
    print("---------------------------")
    print(str, ":", int((datetime.datetime.now() - start_time).total_seconds() * 1000) / 1000.0, len(dist), sum(dist))


# Run all algoritms
graph = Graph(n, C, adjacents)
debug = True if '-v' in sys.argv else False
print(' Start execute dijkstra algorithms')
print_result("heapq", datetime.datetime.now(), graph.dijkstra_naive(0))
print_result("Radix level1", datetime.datetime.now(), graph.dijkstra_radix(0, debug=debug))
print_result("Radix level2", datetime.datetime.now(), graph.dijkstra_radix(0, level='Two level', debug=debug))
print_result("Fib. Heap", datetime.datetime.now(), graph.dijkstra_radix(0, level='Two level + Fibonacci Heap', debug=debug))
