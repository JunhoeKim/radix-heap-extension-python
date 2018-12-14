from doubly_list import DoublyList, Node
from collections import namedtuple
from radix_heap_2 import RadixHeap2

import math

NodeData = namedtuple('NodeData', 'label key')

class FibonacciHeap():
  def __init__(self, n, C, K):
    self.n = n
    self.K = K
    self.B = int(math.ceil(math.log(C + 1, K)) + 1)
    self.radixHeap = RadixHeap2(n, C, K)
    self.min_node = None

    # a lookup table of information of nodes
    self.nodes = [None] * n
    self.S = [set() for x in range(self.B * self.K)]
    self.active_roots = DoublyList()
    self.passive_roots = DoublyList()
    self.rank_nodes = [None] * n

  def insert(self, label, d):
    # Insert a labeled node to radix heap
    b, k, _ = self.radixHeap._insert(label, self.B - 1, d)
    self.radixHeap.len += 1
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

  def decrease(self, label, d):
    # Decrease a labeled node
    self.radixHeap.decrease(label, d)

    b, k, _ = self.radixHeap.node_table[label]
    key = b * self.K + k
    node = self.nodes[label]
    prev_key = node.data.key

    # Update a new key of heap node
    node.data = NodeData(label=label, key=key)
    self._update_min(node)

    # If heap condition is violated, do link cut process
    if node.parent != None and node.parent.data.key > node.data.key:
      parent = node.parent
      self._cut(node)
      self._cascading_cut(parent)

    # Remove the node from the previous set
    self.S[prev_key].remove(label)
    # If there are remaining nodes in the previous segment, assign a new node as a representative
    if len(self.S[prev_key]) > 0 and node.active == True:
      new_representative = self.nodes[next(iter(self.S[prev_key]))]
      new_representative.active = True
      self.passive_roots.remove(new_representative)
      self.active_roots.append_node(new_representative)

    # Move the node to the new set
    self.S[key].add(label)

    # If the new set already has a representative, remove a node as a representative
    if len(self.S[key]) and node.active == True > 1:
      node.active = False
      self.active_roots.remove(node)
      self.passive_roots.append_node(node)

    # If the new set is empty, assign the node as a representative
    if len(self.S[key]) == 1 and node.active == False:
      node.active = True
      self.passive_roots.remove(node)
      self.active_roots.append_node(node)

  def delete_min(self):
    # print([x.key for x in self.active_roots.get_items()])
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
      print('here')
      self._extract_min_in_tree()
      return self.radixHeap.delete_min()

    else:
      temp_nodes, min_index, target_info = self.radixHeap.redistribute_segment(b, k)
      self.S[min_key] = set()
      min_label = temp_nodes[min_index].data[0]
      if len(target_info) > 0:
        # If the actual minimum node is in active trees
        if min_label == self.min_node.data.label:
          # Redistribute
          self._redistribute_nodes(target_info)
          # Remove the remaining minimum node and do linking operation
          print('here1')
          self._extract_min_in_tree()
        else:
          # Insert the node that was in the active root first
          prev_active_node_index = [i for i, target in enumerate(target_info) if target[2].data[0] == self.min_node.data.label][0]
          target = target_info[prev_active_node_index]
          node_key = target[0] * self.K + target[1]
          self.S[node_key].add(target[2].data[0])
          self.min_node.data = NodeData(label=self.min_node.data.label, key=node_key)
          # Redistribute
          self._redistribute_nodes(target_info)
          # Remove minimum node which is not a representative from the passive trees and do linking operation
          self.passive_roots.remove(self.nodes[min_label])
          self._consolidate()
      # If there is only one node in the minimum key set, just extract min node and do linking operation
      else:
        print('here2')
        print([x.key for x in self.active_roots.get_items()])
        print([x.key for x in self.passive_roots.get_items()])
        self.radixHeap.print_buckets()
        self._extract_min_in_tree()
    return self.radixHeap.node_table[min_label][2].data
    
  def __len__(self):
    return len(self.radixHeap)

  def _extract_min_in_tree(self):
    min_node = self.min_node
    self.min_node = None
    deleted_node = self.active_roots.remove(min_node)

    # Update children to active root
    children = deleted_node.children
    while children.len > 0:
      self.active_roots.append_node(children.pop())

    self._consolidate()

  def _cut(self, node):
    parent = node.parent
    parent.rank -= 1
    parent.children.remove(node)
    self.active_roots.append_node(node)
    node.parent = None
    node.mark = False

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
    print(len(active_roots))
    self.min_node = active_roots[0] if len(active_roots) > 0 else None
    max_rank = 0
    for root in active_roots:
      rank = root.rank
      new_root = root

      if self.rank_nodes[rank] != None:
        prev_node = self.rank_nodes[rank]
        if root.data.key > prev_node.data.key:
          new_root = self._link(root, prev_node)
        else:
          new_root = self._link(prev_node, root)

        self.rank_nodes[rank] = None
        self.rank_nodes[rank + 1] = new_root
        if max_rank < rank + 1:
          max_rank = rank + 1
      if root.data.label == 84045:
        print('root', root.data)
        print(self.min_node.data)
        print('new_root', new_root.data)
      self._update_min(new_root)

    for i in range(max_rank):
      self.rank_nodes[i] = None

  def _update_min(self, node):
    if self.min_node == None or self.min_node.data.key > node.data.key:
      self.min_node = node

  def _redistribute_nodes(self, target_info):
    for target in target_info:

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
        # if self.nodes[target_label].data.label == 84045:
        #   print('84045', self.nodes[target_label].data)
        #   print('min_node', self.min_node.data)
        #   print([x.key for x in self.active_roots.get_items()])

  def _link(self, x, y):
    # Convert root x to child of y
    self.active_roots.remove(x)
    y.children.append_node(x)
    y.rank += 1
    x.parent = y
    y.mark = False
