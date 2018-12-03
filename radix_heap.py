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
    self.bucket_indices = [(self.B, None) for i in range(self.n)]
    self.bucket_activates = [True for i in range(self.B)]
    self.len = 0

  def insert(self, label, d):
    self._insert(label, self.B - 1, d)
    # print('insert', self.buckets)
    self.len += 1

  def decrease(self, label, d):
    # print('decrease', self.buckets)
    bucket_index, node = self.bucket_indices[label]
    self.buckets[bucket_index].remove(node)
    self._insert(label, bucket_index, d)

  def _insert(self, label, start_index, d):
    bucket_index_offset = 0
    for i in range(start_index + 1):
      bucket_index = start_index - i

      if self.bucket_activates[bucket_index] == False:
        bucket_index_offset += 1
        continue

      if d > self.u[bucket_index]:
        curr_index = bucket_index + bucket_index_offset
        curr_bucket = self.buckets[curr_index]
        node = curr_bucket.append((label, d))
        self.bucket_indices[label] = (curr_index, node)
        break

      if self.bucket_activates[bucket_index] == True:
        bucket_index_offset = 0

  def delete_min(self):
    # print('delete min', self.buckets)
    self.len -= 1
    if self.buckets[0].size > 0:
      return self.buckets[0].pop().data
    temp_vertices = []
    min_index = 0
    for i in range(0, self.B):
      if self.buckets[i].size > 0:
        while self.buckets[i].size > 0:
          temp_vertices.append(self.buckets[i].pop())
          if temp_vertices[min_index].data[1] > temp_vertices[len(temp_vertices) - 1].data[1]:
            min_index = len(temp_vertices) - 1
        self._update_u(temp_vertices[min_index].data[1], i)
        for i, node in enumerate(temp_vertices):
          if i != min_index:
            self._insert(node.data[0], i, node.data[1])
        break
    # self.print_buckets()
    return temp_vertices[min_index].data

  def is_empty(self):
    return self.len == 0

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


