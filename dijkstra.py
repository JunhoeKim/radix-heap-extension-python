import sys
import heapq
from radix_heap import RadixHeap
from radix_heap_2 import RadixHeap2
from f_heap import FibonacciHeap
from heap import Heap

class Graph():
    def __init__(self, nodeCount, C, graphList):
        self.n = nodeCount
        self.C = C
        
        # sample data for test
        # self.graph = [
        #     [(1, 12), (3, 14), (4, 20), (2, 0)],
        #     [(0, 12), (3, 4)],
        #     [(0, 0), (4, 8)],
        #     [(0, 14), (1, 4), (4, 5), (5, 3)],
        #     [(0, 20), (2, 8), (3, 5), (5, 9)],
        #     [(3, 3), (4, 9)]
        # ]

        # label, distance
        self.graph = graphList

    # O(mlogn) Implementation
    def dijkstra(self, src):
        dist = [sys.maxsize] * self.n
        dist[src] = 0
        h = []
        heapq.heappush(h, (0, src))

        while len(h) > 0:
            top_vertex = heapq.heappop(h)
            u = top_vertex[1]
            if dist[u] < top_vertex[0]:
                continue

            for edge in self.graph[u]:
                weight = edge[1]
                v = edge[0]
                if dist[v] > dist[u] + weight:
                    dist[v] = dist[u] + weight
                    heapq.heappush(h, (dist[v], v))

        return dist
        #print("Minheap : " + str(dist))
    
    def naiveComparator(self, a, b):
        if a[1] >= b[1]:
            return True
        else:
            return False

    def dijkstra_naive(self, src):
        dist = [sys.maxsize] * self.n
        dist[src] = 0
        naiveHeap = Heap(self.naiveComparator)

        naiveHeap.add((0, src))

        while not naiveHeap.is_empty():
            top_vertex = naiveHeap.del_min()
            u = top_vertex[1]
            if dist[u] < top_vertex[0]:
                continue

            for edge in self.graph[u]:
                weight = edge[1]
                v = edge[0]
                if dist[v] > dist[u] + weight:
                    dist[v] = dist[u] + weight
                    naiveHeap.add((dist[v], v))

        return dist

    def dijkstra_radix(self, src, level='One Level'):
        radixheap = None
        if level == 'One Level':
            radixheap = RadixHeap(self.n, self.C)
        elif level == 'Two level':
            radixheap = RadixHeap2(self.n, self.C, 2)
        else:
            radixheap = FibonacciHeap(self.n, self.C, 2)
        dist = [self.n * self.C + 1] * self.n
        dist[src] = 0
        radixheap.insert(src, dist[src])

        while len(radixheap) > 0:
            top_vertex = radixheap.delete_min()
            u = top_vertex[0]
            if dist[u] < top_vertex[1]:
                continue

            for edge in self.graph[u]:
                v = edge[0]
                weight = edge[1]
                if dist[v] > dist[u] + weight:
                    if dist[v] == self.n * self.C + 1:
                        dist[v] = dist[u] + weight
                        radixheap.insert(v, dist[v])
                    else:
                        dist[v] = dist[u] + weight
                        radixheap.decrease(v, dist[v])
      
        #print(level + " : " + str(dist))
        if level == "One Level":
            radixheap.printResult()
        return dist

# graph = Graph()
# graph.dijkstra(0)
# graph.dijkstra_radix(0)
# graph.dijkstra_radix(0, level='Two level')
# graph.dijkstra_radix(0, level='Two level + Fibonacci Heap')