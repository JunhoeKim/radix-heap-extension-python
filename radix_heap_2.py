import sys
import heapq
import math
from doubly_list import DoublyList, Node

class RadixHeap2():
  def __init__(self, n, C, K):
    self.n = n
    self.C = C
    self.K = K
    self.B = int(math.ceil(math.log(self.C + 1, self.K)) + 1)
    self.sizes = [K ** i for i in range(1, self.B)] + [self.n * self.C + 1]
    self.u = [-1] + [int(self.K * (self.K ** i - 1) / (self.K - 1) - 1) for i in range(1, self.B)] + [self.n * self.C + 1]
    self.buckets = [[] for i in range(self.B)]
    for i in range(self.B):
      for _ in range(self.K):
        self.buckets[i].append(DoublyList())
    self.bucket_capacities = [0 for i in range(self.B)]
    self.node_table = [(self.B, self.K, None) for i in range(self.n)] 
    self.bucket_activates = [True for i in range(self.B)]
    self.len = 0

  def insert(self, label, d):
    self._insert(label, self.B - 1, d)
    self.len += 1

  def decrease(self, label, d):
    bucket_index, seg_index, node = self.node_table[label]
    self.buckets[bucket_index][seg_index].remove(node)
    self.bucket_capacities[bucket_index] -= 1
    self._insert(label, bucket_index, d)

  def delete_min(self):
    if self.bucket_capacities[0] > 0:
      for i in range(self.K):
        if self.buckets[0][i].size > 0:
          self.bucket_capacities[0] -= 1
          self.len -= 1
          return self.buckets[0][i].pop().data

    temp_vertices = []
    min_index = 0
    for i in range(0, self.B):
      if self.bucket_capacities[i] > 0:
        for j in range(self.K):
          if self.buckets[i][j].size > 0:
            temp_vertices, min_index, _ = self.redistribute_segment(i, j)
            break
        else:
          continue
        break
    return temp_vertices[min_index].data

  def redistribute_segment(self, i, j):
    self.len -= 1
    temp_vertices = []
    min_index = 0
    while self.buckets[i][j].size > 0:
      temp_vertices.append(self.buckets[i][j].pop())
      self.bucket_capacities[i] -= 1
      if temp_vertices[min_index].data[1] > temp_vertices[len(temp_vertices) - 1].data[1]:
        min_index = len(temp_vertices) - 1
    self._update_u(temp_vertices[min_index].data[1], i, j)
    moved_info = []
    for idx, node in enumerate(temp_vertices):
      if idx != min_index:
        moved_info.append(self._insert(node.data[0], i, node.data[1]))

    return temp_vertices, min_index, moved_info


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
        curr_k = self._compute_k(curr_index, d)
        curr_segment = curr_bucket[curr_k]
        self.bucket_capacities[curr_index] += 1
        node = curr_segment.append((label, d))
        self.node_table[label] = (curr_index, curr_k, node)
        return self.node_table[label]
      
      if self.bucket_activates[bucket_index] == True:
        bucket_index_offset = 0

  def _compute_k(self, bucket_index, d):
    if bucket_index == self.B - 1:
      return 0
    k = self.K - int(math.floor((self.u[bucket_index + 1] - d) / (self.K ** bucket_index))) - 1
    return k

  def _compute_upper_k(self, bucket_index, k):
    return self.u[bucket_index + 1] - (self.K - k - 1) * self.K ** bucket_index

  def is_empty(self):
    return self.len == 0

  def _update_u(self, d, j, k):
    self.u[0] = d - 1
    upper_segment = self._compute_upper_k(j, k)
    for i in range(1, j + 1):
      self.u[i] = min(self.u[i - 1] + self.sizes[i], upper_segment)
      if self.u[i] <= self.u[i - 1]:
        self.bucket_activates[i] = False
      else:
        self.bucket_activates[i] = True

  def _get_real_cap(self):
    real_cap = [[] for x in range(self.B)]
    for i in range(self.B):
      for j in range(self.K):
        real_cap[i].append((j, self.buckets[i][j].size))
    return real_cap
        
  def print_buckets(self):
    for i, bucket in enumerate(self.buckets):
      print("bucket " + str(i))
      for j, segment in enumerate(bucket):
        print("segment " + str(j) + str(segment.get_items()))