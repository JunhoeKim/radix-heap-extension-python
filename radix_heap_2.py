import sys
import heapq
import math
from doubly_list import DoublyList, Node

'''
An class of Two level radix heap for supervising labeled nodes.

It provides the three heap operations as follows.
 * insert(label, d): Insert the labeled node to the heap with its label and distance.
 * decrease(label, d): Pick up the already inserted node from the heap and insert again according to a new distance.
 * delete_min(): Extract the node which has a minimum distance to make it scanned.

It overrides ``__len__``, that provides whether heap is empty or not.

Time complexity: O(m + nlogC/(loglogC))
m: the number of edges
n: the number of nodes
C: the maximum distance of one edge

'''
class RadixHeap2():
  def __init__(self, n, C, K, debug=False):

    # the number of segments for each bucket (hyper parameter)
    self.K = K

    # Variables that samely used in the one level heap
    self.n = n
    self.C = C
    self.B = int(math.ceil(math.log(self.C + 1, self.K)) + 1)
    self.sizes = [K ** i for i in range(1, self.B)] + [self.n * self.C + 1]
    self.u = [-1] + [int(self.K * (self.K ** i - 1) / (self.K - 1) - 1) for i in range(1, self.B)] + [self.n * self.C + 1]
    self.buckets = [[DoublyList() for i in range(self.K)] for j in range(self.B)]
    self.bucket_availables = [True for i in range(self.B)]
    # Stores total length for each bucket
    self.bucket_lens = [0 for i in range(self.B)]
    self.node_table = [(self.B, self.K, None) for i in range(self.n)] 
    self.len = 0
    self.debug = debug

  def insert(self, label, d):
    self._insert(label, self.B - 1, d)
    self.len += 1
    if self.debug == True:
      self.print_buckets('insert label : %s, distance: %s' % (label, d))

  def decrease(self, label, d):
    b, k, node = self.node_table[label]
    self.buckets[b][k].remove(node)
    self.bucket_lens[b] -= 1
    self._insert(label, b, d)
    if self.debug == True:
      self.print_buckets('decrease label: %s, distance: %s' % (label, d))

  def delete_min(self):
    # If the first bucket is not empty, 
    # find non empty segment then pop and return the node
    if self.bucket_lens[0] > 0:
      for i in range(self.K):
        if self.buckets[0][i].len > 0:
          self.bucket_lens[0] -= 1
          self.len -= 1
          min_node = self.buckets[0][i].pop()
          if self.debug:
            self.print_buckets('delete min label: %s, distance: %s' % min_node.data)
          return min_node.data

    min_node = None
    # Find left most non empty segment, find minimum node, reset upper bounds, redistribute
    for i in range(0, self.B):
      if self.bucket_lens[i] > 0:
        for j in range(self.K):
          if self.buckets[i][j].len > 0:
            min_node, _ = self._redistribute(i, j)
            break
        else:
          continue
        break

    if self.debug:
      self.print_buckets('delete min label: %s, distance: %s' % min_node.data)
    return min_node.data

  def _redistribute(self, b, k):

    self.len -= 1
    moved_nodes = []
    min_index = 0
    # Extract all nodes and find minimum node at the same time
    while self.buckets[b][k].len > 0:
      moved_nodes.append(self.buckets[b][k].pop())
      self.bucket_lens[b] -= 1
      if moved_nodes[min_index].data[1] > moved_nodes[len(moved_nodes) - 1].data[1]:
        min_index = len(moved_nodes) - 1
    # Update upper bound according to the distance of minimum node
    self._update_u(moved_nodes[min_index].data[1], b, k)
    redistributed_info = []
    # Insert the nodes except the minmum node, store redistributed information for each node
    for index, node in enumerate(moved_nodes):
      if index != min_index:
        redistributed_info.append(self._insert(node.data[0], b, node.data[1]))

    return moved_nodes[min_index], redistributed_info

  def _insert(self, label, start_index, d):
    b_offset = 0
    # Find the appropriate bucket index according to the upper bounds
    for i in range(start_index + 1):
      b = start_index - i

      if self.bucket_availables[b] == False:
        b_offset += 1
        continue

      if d > self.u[b]:
        curr_index = b + b_offset
        curr_bucket = self.buckets[curr_index]
        curr_k = self._compute_k(curr_index, d)
        curr_segment = curr_bucket[curr_k]
        self.bucket_lens[curr_index] += 1
        node = curr_segment.append((label, d))
        self.node_table[label] = (curr_index, curr_k, node)
        return self.node_table[label]
      
      if self.bucket_availables[b] == True:
        b_offset = 0

  # Compute the segment index from the bucket index and distance
  def _compute_k(self, b, d):
    if b == self.B - 1:
      return 0
    k = self.K - int(math.floor((self.u[b + 1] - d) / (self.K ** b))) - 1
    return k

  # Compute the upper bound of the bucket from the index bucket and segment
  def _compute_upper_k(self, b, k):
    return self.u[b + 1] - (self.K - k - 1) * self.K ** b

  def __len__(self):
    return self.len

  def _update_u(self, d, j, k):
    self.u[0] = d - 1
    upper_bound = self._compute_upper_k(j, k)
    for i in range(1, j + 1):
      self.u[i] = min(self.u[i - 1] + self.sizes[i - 1], upper_bound)
      if self.u[i] <= self.u[i - 1]:
        self.bucket_availables[i] = False
      else:
        self.bucket_availables[i] = True

  def print_buckets(self, op_name):
    title_str = '* ------ Operation: %s ------- *' % op_name 
    print('\n' + title_str)
    print('\n Bucket states : ')
    for i, x in enumerate(self.buckets):
      if i < len(self.buckets) - 1:
        print(' ' + str((self.u[i], self.u[i + 1])) + ' ' + self._str_bucket(x))
      else:
        print(' ' + str((self.u[i], '~')) + ' ' + self._str_bucket(x))

    print ('\n* ' + '-' * (len(title_str) - 4) + ' *')

  def _str_bucket(self, bucket):
    result = ''
    for index in range(self.K):
      result += '\n    ' + str(index) + ': ' + str(bucket[index].get_items())
    return result