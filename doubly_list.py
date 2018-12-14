class Node(object):
  def __init__(self, data):
    self.data = data 
    self.parent = None
    self.prev = None
    self.next = None
    self.children = DoublyList() 
    self.rank = 0
    self.mark = False
    self.active = False

class DoublyList(object):
 
  def __init__(self):
    self.head = None
    self.tail = None
    self.len = 0
 
  def append(self, data):
    new_node = Node(data)
    return self.append_node(new_node)

  def append_node(self, node):
    self.len += 1
    if self.head == None:
      self.head = self.tail = node
    else:
      node.prev = self.tail
      node.next = None
      self.tail.next = node 
      self.tail = self.tail.next
    return node

  def remove(self, node):
    if node == self.head:
      return self.pop()
    else:
      self.len -= 1
      node.prev.next = node.next

      if node.next != None:
        node.next.prev =  node.prev
      if self.tail == node:
        self.tail = node.prev

    node.next = None
    node.prev = None
    return node

  def find_mean(self):
    curr = self.head
    min_node = self.head
    while curr.next != None:
      curr = curr.next
      if min_node.data[1] > curr.data[1]:
        min_node = curr

    return min_node

  def pop(self):
    self.len -= 1
    curr = self.head
    if self.len == 0:
      self.head = None
      self.tail = None
    else:
      self.head = curr.next
      self.head.prev = None

    curr.next = None
    curr.prev = None
    return curr

  def get_items(self):

    if self.len == 0:
      return []

    items = []
    curr = self.head 
    items.append(curr.data)

    while curr.next != None:
      curr = curr.next
      items.append(curr.data)

    return items

  def get_nodes(self):
    if self.len == 0:
      return []

    nodes = []
    curr = self.head 
    nodes.append(curr)
    while curr.next != None:
      curr = curr.next
      nodes.append(curr)

    return nodes