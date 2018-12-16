from doubly_list import DoublyList, Node
from collections import namedtuple
from radix_heap_2 import RadixHeap2

import math

NodeData = namedtuple('NodeData', 'label key')
'''
An class of Fibonacci heap extension for heap operation.
It uses 2 level radix heap for supervising labeled nodes.
The Fibonacci heap that consists of active trees and passive trees supervises minimum segment index.
Active trees consist of representatives for each segment so that it can control all segments with only active trees.

It provides the three heap operations as follows.
 * insert(label, d): Insert the labeled node to the heap with its label and distance.
 * decrease(label, d): Pick up the already inserted node from the heap and insert again according to a new distance.
 * delete_min(): Extract the node which has a minimum distance to make it scanned.

It overrides ``__len__``, that provides whether heap is empty or not.

Time complexity: O(m + n * sqrt(logC))
m: the number of edges
n: the number of nodes
C: the maximum distance of one edge

'''

class FibonacciHeap():
  def __init__(self, n, C, K, debug=False):
    self.n = n
    self.K = K
    self.B = int(math.ceil(math.log(C + 1, K)) + 1)
    self.radix_heap = RadixHeap2(n, C, K)

    # Node that has minimum segment index
    self.min_node = None

    # a lookup table of information of nodes
    self.nodes = [None] * n
    self.S = [set() for x in range(self.B * self.K)]
    self.active_roots = DoublyList()
    self.passive_roots = DoublyList()
    self.rank_nodes = [None] * n
    self.debug = debug
    self.radix_heap.debug = debug
    self.debug = True

  def insert(self, label, d):
    # Insert a labeled node to radix heap
    b, k, _ = self.radix_heap._insert(label, self.B - 1, d)
    self.radix_heap.len += 1
    # Retrieve heap key from bucket index (b) and segment index (k)
    key = b * self.K + k 
    # Append a new node to root trees
    new_node = Node(NodeData(label=label, key=key))
    self.nodes[label] = new_node
    self.S[key].add(label)

    # If there is only one element in the set, set the new node as a representative
    if len(self.S[key]) == 1:
      new_node.active = True
      self.active_roots.append_node(new_node) 
      # Update min node
      self._update_min(new_node)
    else:
      self.passive_roots.append_node(new_node)

    if self.debug == True:
      self.print_heap('insert label : %s, distance: %s' % (label, d))

  def decrease(self, label, d):
    # Decrease a labeled node
    self.radix_heap.decrease(label, d)

    b, k, _ = self.radix_heap.node_table[label]
    key = b * self.K + k
    node = self.nodes[label]
    prev_key = node.data.key
    # Update a new key of heap node
    node.data = NodeData(label=label, key=key)

    # If heap condition is violated, do link cut process
    if node.parent != None and node.parent.data.key > node.data.key:
      parent = node.parent
      self._cut(node)
      self._cascading_cut(parent)

    # Remove the node from the previous set
    self.S[prev_key].remove(label)
    # If there are remaining nodes in the previous segment, assign a new node as a representative
    new_representative = None
    if len(self.S[prev_key]) > 0 and node.active == True:
      new_representative = self.nodes[next(iter(self.S[prev_key]))]
      new_representative.active = True
      self.passive_roots.remove(new_representative)
      self.active_roots.append_node(new_representative)

    # Move the node to the new set
    self.S[key].add(label)

    # If the new set already has a representative, remove a node as a representative
    if len(self.S[key]) > 1 and node.active == True:
      if self.min_node.data.label == label:
        self.min_node = None
      node.active = False

      # If the previous position of node is not root, it links the children to its parent.
      if node.parent != None:
        parent = node.parent
        parent.children.remove(node)
        node.parent = None
        while node.children.len > 0:
          child = node.children.pop()
          child.parent = parent
          parent.children.append_node(child)
      # Else, it appends the children to active roots
      else:
        self.active_roots.remove(node)
        while node.children.len > 0:
          child = node.children.pop()
          child.parent = None
          self.active_roots.append_node(child)
          self._update_min(child)

      self.passive_roots.append_node(node)

    # If the new set is empty, assign the node as a representative
    if len(self.S[key]) == 1 and node.active == False:
      node.active = True
      self.passive_roots.remove(node)
      self.active_roots.append_node(node)

    self._update_min(node)

    # If there is a new representative, update min
    if new_representative != None:
      self._update_min(new_representative)

    if self.debug == True:
      self.print_heap('decrease label : %s, distance: %s' % (label, d))
    

  def delete_min(self):
    min_key = self.min_node.data.key
    b = min_key // self.K
    k = min_key - b * self.K

    # If the minimum node is in a first segment, there is no redistribution process
    if min_key == 0:
      self.S[min_key].remove(self.min_node.data.label)

      # If there are remaining nodes in the previous segment, assign a new node as a representative
      if len(self.S[min_key]) > 0:
        new_representative = self.nodes[next(iter(self.S[min_key]))]
        new_representative.active = True
        self.passive_roots.remove(new_representative)
        self.active_roots.append_node(new_representative)

      # Extract min and do a linking operation
      self._extract_min_in_tree()
      result = self.radix_heap.delete_min()

      if self.debug == True:
        self.print_heap('delete min label : %s, distance: %s' % result)

      return result

    else:
      min_node, redistributed_info = self.radix_heap._redistribute(b, k)
      self.S[min_key] = set()
      min_label = min_node.data[0]
      if len(redistributed_info) > 0:
        # If the actual minimum node is in active trees
        if min_label == self.min_node.data.label:
          # Redistribute
          self._redistribute(redistributed_info)
          # Remove the remaining minimum node and do linking operation
          self._extract_min_in_tree()
        else:
          # Insert the node that was in the active root first
          prev_active_node_index = [i for i, target in enumerate(redistributed_info) if target[2].data[0] == self.min_node.data.label][0]
          target = redistributed_info[prev_active_node_index]
          node_key = target[0] * self.K + target[1]
          self.S[node_key].add(target[2].data[0])
          self.min_node.data = NodeData(label=self.min_node.data.label, key=node_key)
          # Redistribute
          self._redistribute(redistributed_info)
          # Remove minimum node which is not a representative from the passive trees and do linking operation
          self.passive_roots.remove(self.nodes[min_label])
          self._consolidate()
      # If there is only one node in the minimum key set, just extract min node and do linking operation
      else:
        self._extract_min_in_tree()
    
    result = self.radix_heap.node_table[min_label][2].data
    if self.debug:
      self.print_heap('delete min label : %s, distance: %s' % result) 
    return result
    
  def __len__(self):
    return len(self.radix_heap)

  # Extract minimum node to delete, do consolidate operation
  def _extract_min_in_tree(self):
    min_node = self.min_node
    self.min_node = None
    deleted_node = self.active_roots.remove(min_node)

    # Update children to active root
    children = deleted_node.children
    while children.len > 0:
      child = children.pop()
      child.parent = None
      self.active_roots.append_node(child)

    self._consolidate()

  # Cut the target node from the parent and append to the active tree roots
  def _cut(self, node):
    parent = node.parent
    parent.children.remove(node)
    self.active_roots.append_node(node)
    node.parent = None
    node.mark = False

  # If the mark of parent node is true, recursively call cut operation
  def _cascading_cut(self, node):
    parent = node.parent
    # If node is not a root
    if parent != None:
      if parent.mark == False and parent.children.len > 0:
        parent.mark = True
      else:
        self._cut(node)
        self._cascading_cut(parent)

  def _consolidate(self):
    # Do linking operations so that no active root with the same rank exists
    active_roots = self.active_roots.get_nodes()
    self.min_node = active_roots[0] if len(active_roots) > 0 else None
    max_rank = 0
    for root in active_roots:
      rank = root.children.len
      new_root = root

      # Do linking operation until there is an empty space in rank node array
      while self.rank_nodes[rank] != None:
        prev_node = self.rank_nodes[rank]
        if new_root.data.key > prev_node.data.key:
          new_root = self._link(new_root, prev_node)
        else:
          new_root = self._link(prev_node, new_root)

        self.rank_nodes[rank] = None
        rank += 1

      self.rank_nodes[rank] = new_root
      if max_rank < rank:
        max_rank = rank

      self._update_min(new_root)

    for i in range(max_rank + 1):
      self.rank_nodes[i] = None

  # Select a minimum node from active roots
  def _update_min(self, node):
    if node.active == True and (self.min_node == None or self.min_node.data.key > node.data.key):
      self.min_node = node

  # Redistribute passive nodes to a new set
  # If there is no representative in the set, assign the passive nodes as representatives
  def _redistribute(self, redistributed_info):
    for target in redistributed_info:
      target_label = target[2].data[0]
      target_key = target[0] * self.K + target[1]
      target_node = self.nodes[target_label]

      # Do not consider remain node
      if target_node.active == True:
        continue

      self.S[target_key].add(target_label)
      target_node.data = NodeData(label=target_label, key=target_key)
      if len(self.S[target_key]) == 1:
        target_node.active = True
        self.passive_roots.remove(target_node)
        self.active_roots.append_node(target_node)

  def _link(self, x, y):
    # Convert root x to child of y
    self.active_roots.remove(x)
    y.children.append_node(x)
    x.parent = y
    y.mark = False
    return y


  def print_heap(self, op_name):
    title_str = '* ------ Operation: %s ------- *' % op_name 
    print('\n' + title_str)
    print('\n Active trees : ')
    for node in self.active_roots.get_nodes():
      self._print_node(node, 0)

    print('\n Passive trees : ')
    for node in self.passive_roots.get_nodes():
      self._print_node(node, 0)

    print ('\n* ' + '-' * (len(title_str) - 4) + ' *')

  def _print_node(self, node, height):
    print('  ' * height + '->' + str(node.data))
    for child in node.children.get_nodes():
      self._print_node(child, height + 1)