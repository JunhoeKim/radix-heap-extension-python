from doubly_list import DoublyList, Node
from collections import namedtuple
from radix_heap_2 import RadixHeap2

import math

NodeData = namedtuple('NodeData', 'label seg_index')

class TreeNode(object):
  def __init__(self, data):
    self.data = data 
    self.parent = None
    self.prev = None
    self.next = None
    self.child_list = DoublyList() 
    self.rank = 0
    self.mark = False
    self.active = False

class FibonacciHeap():
  def __init__(self, n, C, K):
    self.n = n
    self.K = K
    self.B = int(math.ceil(math.log(C + 1, K)) + 1)
    self.radixHeap = RadixHeap2(n, C, K)
    self.min_node = None
    self.vertices = [None] * n
    self.S = [set() for x in range(self.B * K)]
    self.active_roots = DoublyList()
    self.roots = DoublyList()

  def insert(self, label, d):
    bucket_index, curr_k, _ =self.radixHeap._insert(label, self.B - 1, d)
    seg_index = bucket_index * self.K + curr_k
    self.radixHeap.len += 1
    # There are no elements in representives of the segment index
    new_node = TreeNode(NodeData(label=label, seg_index=seg_index))
    self.vertices[label] = new_node
    self.S[seg_index].add(label)
    self.roots.append_node(new_node)
    if len(self.S[seg_index]) == 1:
      new_node.active = True
      self.active_roots.append_node(new_node) 
      # update min node
      if self.min_node == None or self.min_node.data.seg_index > new_node.data.seg_index:
        self.min_node = new_node

  def decrease(self, label, d):
    result_data = self.radixHeap.decrease(label, d)
    bucket_index, curr_k, _ = self.radixHeap.bucket_indices[label]
    seg_index = bucket_index * self.K + curr_k
    target_node = self.vertices[label]
    prev_value = target_node.data
    target_node.data = NodeData(label=label, seg_index=seg_index)

    if target_node.parent != None and target_node.parent.data.seg_index > target_node.data.seg_index:
      parent = target_node.parent
      self._cut(target_node)
      self._cascading_cut(parent)

    if self.min_node.data.seg_index > target_node.data.seg_index:
      self.min_node = target_node

    self.S[prev_value.seg_index].remove(label)
    # if there are remaining nodes in the previous segment assign new active tree root node
    if target_node.active == True and len(self.S[prev_value.seg_index]) > 0:
      remain_label = next(iter(self.S[prev_value.seg_index]))
      self.vertices[remain_label].active = True
      self.active_roots.append_node(self.vertices[remain_label])

    self.S[seg_index].add(label)
    if target_node.active == True:
      # move to passive tree
      if len(self.S[seg_index]) > 1:
        target_node.active = False
        self.active_roots.remove(target_node)

    # if a new set is empty, convert target_node to the active node
    if len(self.S[seg_index]) == 1 and target_node.active == False:
      self.active_roots.append_node(target_node)
      target_node.active = True

    return result_data

  def delete_min(self):
    print('--------------delete min')
    min_seg_index = self.min_node.data.seg_index
    bucket_index = min_seg_index // self.K
    relative_seg_index = min_seg_index - bucket_index * self.K
    # If the minimum node is in a first segment
    if min_seg_index == 0:
      self.S[min_seg_index].remove(self.min_node.data.label)
      if len(self.S[min_seg_index]) > 0:
        new_active_node = self.vertices[next(iter(self.S[min_seg_index]))]
        new_active_node.active = True
        self.active_roots.append_node(new_active_node)
      self._extract_min_in_tree()
      return self.radixHeap.delete_min()

    else:
      temp_vertices, min_index, moved_info = self.radixHeap.redistribute_segment(bucket_index, relative_seg_index)
      self.S[min_seg_index] = set()
      min_label = temp_vertices[min_index].data[0]
      if len(moved_info) > 0:
        # if actual minimum node is in active trees
        if min_label == self.min_node.data.label:
          # Redistribute
          for node_info in moved_info:
            moved_label = node_info[2].data[0]
            moved_seg_index = node_info[0] * self.K + node_info[1]
            self.S[moved_seg_index].add(moved_label)
            self.vertices[moved_label].data = NodeData(label=moved_label, seg_index=moved_seg_index)
            if len(self.S[moved_seg_index]) == 1 and self.vertices[moved_label].active == False:
              self.vertices[moved_label].active = True
              self.active_roots.append_node(self.vertices[moved_label])
          self._extract_min_in_tree() 
        else:
          # Insert the node that was in the active root first.
          prev_active_node_index = [i for i, node_info in enumerate(moved_info) if node_info[2].data[0] == self.min_node.data.label][0]
          node_info = moved_info[prev_active_node_index]
          node_seg_index = node_info[0] * self.K + node_info[1]
          self.S[node_seg_index].add(node_info[2].data[0])
          self.min_node.data = NodeData(label=self.min_node.data.label, seg_index=node_seg_index)
          # Redistribute
          for node_info in moved_info:
            moved_label = node_info[2].data[0]
            moved_seg_index = node_info[0] * self.K + node_info[1]
            self.S[moved_seg_index].add(moved_label)
            self.vertices[moved_label].data = NodeData(label=moved_label, seg_index=moved_seg_index)
            if len(self.S[moved_seg_index]) == 1 and self.vertices[moved_label].active == False:
              self.vertices[moved_label].active = True
              self.active_roots.append_node(self.vertices[moved_label])
          # remove minimum vertex in the passive trees
          self.roots.remove(self.vertices[min_label])
          self._consolidate()
      else:
        self._extract_min_in_tree()
    self.radixHeap.print_buckets()
    return self.radixHeap.bucket_indices[min_label][2].data

  def is_empty(self):
    return self.radixHeap.is_empty()

  def _extract_min_in_tree(self):
    min_node = self.min_node
    self.min_node = None
    deleted_node = self.active_roots.remove(min_node)
    self.roots.remove(min_node)

    # update children to active root
    children = deleted_node.child_list
    while children.size > 0:
      self.active_roots.append_node(children.pop())

    self._consolidate()

  def _cut(self, target_node):
    parent = target_node.parent
    parent.rank -= 1
    parent.child_list.remove(target_node)
    self.roots.append_node(target_node)
    if target_node.active:
      self.active_roots.append_node(target_node)
    target_node.parent = None
    target_node.mark = False

  def _cascading_cut(self, target_node):
    parent = target_node.parent
    # target_node is not a root node
    if parent != None:
      if parent.mark == False:
        parent.mark = True
      else:
        self._cut(target_node)
        self._cascading_cut(parent)


  def _consolidate(self):
    rank_nodes = [None] * self.n
    active_roots = self.active_roots.get_nodes()
    self.min_node = active_roots[0] if len(active_roots) > 0 else None
    for i, root in enumerate(active_roots):
      rank = root.rank
      new_root = root

      if rank_nodes[rank] != None:
        prev_node = rank_nodes[rank]
        if root.data.seg_index > prev_node.data.seg_index:
          new_root = self._link(root, prev_node)
        else:
          new_root = self._link(prev_node, root)

        rank_nodes[rank] = None
        rank_nodes[rank + 1] = new_root

      if self.min_node == None or self.min_node.data.seg_index > new_root.data.seg_index:
        self.min_node = new_root

  def _link(self, x, y):
    self.active_roots.remove(x)
    y.child_list.append_node(x)
    y.rank += 1
    x.parent = y
    y.mark = False
