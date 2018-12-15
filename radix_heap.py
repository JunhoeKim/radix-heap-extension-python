import sys
import heapq
import math
from doubly_list import DoublyList, Node
import datetime

'''
An class of One level radix heap for supervising labeled nodes.

It provides the three heap operations as follows.
 * insert(label, d): Insert the labeled node to the heap with its label and distance.
 * decrease(label, d): Pick up the already inserted node from the heap and insert again according to a new distance.
 * delete_min(): Extract the node which has a minimum distance to make it scanned.

It overrides ``__len__``, that provides whether heap is empty or not.

Time complexity: O(m + nlogC)
m: the number of edges
n: the number of nodes
C: the maximum distance of one edge

'''
class RadixHeap():
  
  def __init__(self, n, C, debug=False):

    self.n = n
    self.C = C
    # The number of buckets
    self.B = int(math.ceil(math.log(self.C + 1, 2)) + 2)
    # Set the range of each bucket
    self.sizes = [1] + [2 ** (i - 1) for i in range(1, self.B)] + [self.n * self.C + 1]
    # Each bucket consists of a doubly list
    self.buckets = [DoublyList() for x in range(self.B)]
    # The upper bound of each buckets which determines the position of the bucket to be inserted
    self.u = [-1] + [2 ** i - 1 for i in range(self.B - 1)] + [self.n * self.C + 1]
    # A look up table for each node
    self.node_table = [(self.B, None) for i in range(self.n)]
    # It stores an activation of each bucket
    self.bucket_availables = [True for i in range(self.B)]
    # The number of labeled nodes in the heap
    self.len = 0

    # Variables for statistics
    self.insertCallCount = 0
    self.decreseCallCount = 0
    self._insertCallCount = 0
    self.delete_minCallCount = 0
    self.updateUCallCount = 0
    self.insertTime = 0
    self.deleteMinTime = 0
    self.debug = debug
    if self.debug:
      self.print_buckets('init')

  def printResult(self):
    # print(self.insertCallCount, self.decreseCallCount, self._insertCallCount, self.delete_minCallCount, self.updateUCallCount)
    # print(self.insertTime / 1000.0, self.deleteMinTime/1000.0)
    return

  # Find an appropraite bucket to insert the node from the index of the last bucket
  def insert(self, label, d):
    self.insertCallCount += 1
    self._insert(label, self.B - 1, d)
    self.len += 1
    if self.debug:
      self.print_buckets('insert label : %s, distance: %s' % (label, d))
    

  # Remove the node from the original bucket and insert the node from the index of the bucket
  def decrease(self, label, d):
    self.decreseCallCount += 1
    b, node = self.node_table[label]
    self.buckets[b].remove(node)
    self._insert(label, b, d)
    if self.debug:
      self.print_buckets('decrease label: %s, distance: %s' % (label, d))

  def _insert(self, label, start_index, d):
    st = datetime.datetime.now()
    self._insertCallCount += 1
    b_offset = 0
    # Find the appropriate bucket index according to the upper bounds
    for i in range(start_index + 1):
      b = start_index - i

      # Skip inactive buckets
      if self.bucket_availables[b] == False:
        b_offset += 1
        continue

      if d > self.u[b]:
        curr_index = b + b_offset
        curr_bucket = self.buckets[curr_index]
        node = curr_bucket.append((label, d))
        self.node_table[label] = (curr_index, node)
        break

      if self.bucket_availables[b] == True:
        b_offset = 0
    self.insertTime += int((datetime.datetime.now() - st).total_seconds() * 1000)

  # Remove the minimum node from the left most bucket and redistribute the nodes from the bucket
  def delete_min(self):
    st = datetime.datetime.now()
    self.delete_minCallCount += 1
    self.len -= 1
    # If the first bucket is not empty, just pop and return the node
    if self.buckets[0].len > 0:
      self.deleteMinTime += int((datetime.datetime.now() - st).total_seconds() * 1000)
      min_node = self.buckets[0].pop()
      if self.debug:
        self.print_buckets('delete min label: %s, distance: %s' % min_node.data)
      return min_node.data

    moved_nodes = []
    min_index = 0
    # Find left most non empty bucket, find minimum node, reset upper bounds, redistribute
    for i in range(self.B):
      if self.buckets[i].len > 0:

        # Extract all nodes and find minimum node at the same time
        while self.buckets[i].len > 0:
          moved_nodes.append(self.buckets[i].pop())
          if moved_nodes[min_index].data[1] > moved_nodes[len(moved_nodes) - 1].data[1]:
            min_index = len(moved_nodes) - 1

        # Update upper bound according to the distance of minimum node
        self._update_u(moved_nodes[min_index].data[1], i)

        # Insert the nodes except the minmum node
        for j, node in enumerate(moved_nodes):
          if j != min_index:
            self._insert(node.data[0], i, node.data[1])
        break

    self.deleteMinTime += int((datetime.datetime.now() - st).total_seconds() * 1000)

    if self.debug:
      self.print_buckets('delete min label: %s, distance: %s' % moved_nodes[min_index].data)
    return moved_nodes[min_index].data

  # Update upper bounds using the mimimum distance and sizes
  def _update_u(self, d, j):
    self.updateUCallCount += 1
    self.u[0] = d - 1
    self.u[1] = d
    for i in range(2, j + 1):
      self.u[i] = min(self.u[i - 1] + self.sizes[i], self.u[j + 1])
      self.bucket_availables[i] = False if self.u[i] <= self.u[i - 1] else True

  def __len__(self):
    return self.len

  def print_buckets(self, op_name):
    title_str = '* ------ Operation: %s ------- *' % op_name 
    print('\n' + title_str)
    print('\n Bucket states : ')
    for i, x in enumerate(self.buckets):
      if i < len(self.buckets) - 1:
        print(' ' + str((self.u[i], self.u[i + 1])) + ' ' + str(x.get_items()))
      else:
        print(' ' + str((self.u[i], '~')) + ' ' + str(x.get_items()))

    print ('\n* ' + '-' * (len(title_str) - 4) + ' *')


