import sys
import heapq
import math
from doubly_list import DoublyList, Node

class RadixHeap():
  
  def __init__(self, n, C):
    self.n = n
    self.C = C
    self.B = int(math.ceil(math.log(self.C + 1, 2)) + 2)
    self.sizes = [1] + [2 ** (i - 1) for i in range(1, self.B)] + [self.n * self.C + 1]
    self.buckets = [DoublyList() for x in range(self.B)]
    self.u = [-1] + [2 ** i - 1 for i in range(self.B - 1)] + [self.n * self.C + 1]
    self.node_table = [(self.B, None) for i in range(self.n)]
    self.bucket_activates = [True for i in range(self.B)]
    self.len = 0

  def insert(self, label, d):
    self._insert(label, self.B - 1, d)
    self.len += 1

  def decrease(self, label, d):
    b, node = self.node_table[label]
    self.buckets[b].remove(node)
    self._insert(label, b, d)

  def _insert(self, label, start_index, d):
    b_offset = 0
    # Find the appropriate bucket index according to upper bound values (u)
    for i in range(start_index + 1):
      b = start_index - i

      # Skip inactive buckets
      if self.bucket_activates[b] == False:
        b_offset += 1
        continue

      if d > self.u[b]:
        curr_index = b + b_offset
        curr_bucket = self.buckets[curr_index]
        node = curr_bucket.append((label, d))
        self.node_table[label] = (curr_index, node)
        break

      if self.bucket_activates[b] == True:
        b_offset = 0

  def delete_min(self):
    self.len -= 1
    # If the first bucket is not empty, just pop and return the node
    if self.buckets[0].len > 0:
      return self.buckets[0].pop().data
    temp_nodes = []
    min_index = 0
    # Find left most non empty bucket, find minimum node, reset upper bounds, redistribute
    for i in range(0, self.B):
      if self.buckets[i].len > 0:
        while self.buckets[i].len > 0:
          temp_nodes.append(self.buckets[i].pop())
          if temp_nodes[min_index].data[1] > temp_nodes[len(temp_nodes) - 1].data[1]:
            min_index = len(temp_nodes) - 1
        self._update_u(temp_nodes[min_index].data[1], i)
        for i, node in enumerate(temp_nodes):
          if i != min_index:
            self._insert(node.data[0], i, node.data[1])
        break
    return temp_nodes[min_index].data

  def __len__(self):
    return self.len

  def _update_u(self, d, j):
    self.u[0] = d - 1
    self.u[1] = d
    for i in range(2, j + 1):
      self.u[i] = min(self.u[i - 1] + self.sizes[i], self.u[j])
      if self.u[i] <= self.u[i - 1]:
        self.bucket_activates[i] = False
      else:
        self.bucket_activates[i] = True

  def print_buckets(self):
    print('\n------print buckets-------')
    for i, x in enumerate(self.buckets):
      if i < len(self.buckets) - 1:
        print((self.u[i], self.u[i + 1]), x.get_items())
      else:
        print((self.u[i], '~'), x.get_items())

    print('---------------------------\n')


