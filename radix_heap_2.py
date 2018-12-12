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
    self.buckets = [[DoublyList() for i in range(self.K)] for j in range(self.B)]
    self.bucket_capacities = [0 for i in range(self.B)]
    self.bucket_activates = [True for i in range(self.B)]
    self.node_table = [(self.B, self.K, None) for i in range(self.n)] 
    self.len = 0

  def insert(self, label, d):
    self._insert(label, self.B - 1, d)
    self.len += 1

  def decrease(self, label, d):
    b, k, node = self.node_table[label]
    self.buckets[b][k].remove(node)
    self.bucket_capacities[b] -= 1
    self._insert(label, b, d)

  def delete_min(self):

    # If the first bucket is not empty, 
    # find non empty segment then pop and return the node
    if self.bucket_capacities[0] > 0:
      for i in range(self.K):
        if self.buckets[0][i].len > 0:
          self.bucket_capacities[0] -= 1
          self.len -= 1
          return self.buckets[0][i].pop().data

    temp_nodes = []
    min_index = 0
    # Find left most non empty segment, find minimum node, reset upper bounds, redistribute
    for i in range(0, self.B):
      if self.bucket_capacities[i] > 0:
        for j in range(self.K):
          if self.buckets[i][j].len > 0:
            temp_nodes, min_index, _ = self.redistribute_segment(i, j)
            break
        else:
          continue
        break
    return temp_nodes[min_index].data

  def redistribute_segment(self, b, k):
    self.len -= 1
    temp_nodes = []
    min_index = 0
    while self.buckets[b][k].len > 0:
      temp_nodes.append(self.buckets[b][k].pop())
      self.bucket_capacities[b] -= 1
      if temp_nodes[min_index].data[1] > temp_nodes[len(temp_nodes) - 1].data[1]:
        min_index = len(temp_nodes) - 1
    self._update_u(temp_nodes[min_index].data[1], b, k)
    target_info = []
    for index, node in enumerate(temp_nodes):
      if index != min_index:
        target_info.append(self._insert(node.data[0], b, node.data[1]))

    return temp_nodes, min_index, target_info


  def _insert(self, label, start_index, d):
    b_offset = 0
    for i in range(start_index + 1):
      b = start_index - i
      if self.bucket_activates[b] == False:
        b_offset += 1
        continue

      if d > self.u[b]:
        curr_index = b + b_offset
        curr_bucket = self.buckets[curr_index]
        curr_k = self._compute_k(curr_index, d)
        curr_segment = curr_bucket[curr_k]
        self.bucket_capacities[curr_index] += 1
        node = curr_segment.append((label, d))
        self.node_table[label] = (curr_index, curr_k, node)
        return self.node_table[label]
      
      if self.bucket_activates[b] == True:
        b_offset = 0

  def _compute_k(self, b, d):
    if b == self.B - 1:
      return 0
    k = self.K - int(math.floor((self.u[b + 1] - d) / (self.K ** b))) - 1
    return k

  def _compute_upper_k(self, b, k):
    return self.u[b + 1] - (self.K - k - 1) * self.K ** b

  def __len__(self):
    return self.len

  def _update_u(self, d, j, k):
    self.u[0] = d - 1
    upper_bound = self._compute_upper_k(j, k)
    for i in range(1, j + 1):
      self.u[i] = min(self.u[i - 1] + self.sizes[i], upper_bound)
      if self.u[i] <= self.u[i - 1]:
        self.bucket_activates[i] = False
      else:
        self.bucket_activates[i] = True

  def print_buckets(self):
    for i, bucket in enumerate(self.buckets):
      print("bucket " + str(i))
      for j, segment in enumerate(bucket):
        print("segment " + str(j) + str(segment.get_items()))