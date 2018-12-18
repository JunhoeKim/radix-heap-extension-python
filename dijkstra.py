import sys
import heapq
from radix_heap import RadixHeap
from radix_heap_2 import RadixHeap2
from f_heap import FibonacciHeap
from heap import Heap

class Graph():
    def __init__(self, n, C, adjacents):
        self.n = n
        self.C = C
        self.adjacents = adjacents

    # O(mlogn) Implementation
    def dijkstra_naive(self, src):
        dist = [sys.maxsize] * self.n
        dist[src] = 0
        h = []
        heapq.heappush(h, (0, src))

        while len(h) > 0:
            top_vertex = heapq.heappop(h)
            u = top_vertex[1]
            if dist[u] < top_vertex[0]:
                continue

            for edge in self.adjacents[u]:
                weight = edge[1]
                v = edge[0]
                if dist[v] > dist[u] + weight:
                    dist[v] = dist[u] + weight
                    heapq.heappush(h, (dist[v], v))

        return dist
    
    def dijkstra_radix(self, src, level='One Level', debug=False):
        radixheap = None
        if level == 'One Level':
            radixheap = RadixHeap(self.n, self.C, debug=debug)
        elif level == 'Two level':
            radixheap = RadixHeap2(self.n, self.C, 4, debug=debug)
        else:
            radixheap = FibonacciHeap(self.n, self.C, 4, debug=debug)
        dist = [self.n * self.C + 1] * self.n
        dist[src] = 0
        radixheap.insert(src, dist[src])

        while len(radixheap) > 0:
            top_vertex = radixheap.delete_min()
            u = top_vertex[0]
            if dist[u] < top_vertex[1]:
                continue

            for edge in self.adjacents[u]:
                v = edge[0]
                weight = edge[1]
                if dist[v] > dist[u] + weight:
                    if dist[v] == self.n * self.C + 1:
                        dist[v] = dist[u] + weight
                        radixheap.insert(v, dist[v])
                    else:
                        dist[v] = dist[u] + weight
                        radixheap.decrease(v, dist[v])
      
        return dist
