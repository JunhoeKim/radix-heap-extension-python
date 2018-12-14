class Heap(object):
    """"
    Attributes:
        heap: List representation of the heap
        compar(p, c): comparator function, returns true if the relation between p and c is parent-chield
    """
    def __init__(self, compar):
        self.heap = []
        self.compar = compar
    def is_empty(self):
        return len(self.heap) == 0
    def _inv_heapify(self, element_id):
        """
        Do heapifying starting from bottom till it reaches the root.
        """
        while element_id > 0:
            if self.compar(self.heap[int(element_id / 2)], self.heap[element_id]):
                return
            self.heap[int(element_id / 2)], self.heap[element_id] = self.heap[element_id], self.heap[int(element_id / 2)]
            element_id = int(element_id / 2)
            # print("inv loop")
    def _heapify(self, element_id):
        """
        Do heepifying starting from the root.
        """
        l = len(self.heap)
        if l == 1:
            return
        while 2 * element_id < l:
            el_id = 2 * element_id
            if 2 * element_id + 1 < l and self.compar(self.heap[element_id * 2 + 1], self.heap[int(element_id * 2)]):
                el_id += 1
            if self.compar(self.heap[element_id], self.heap[el_id]):
                return
            self.heap[element_id], self.heap[el_id] = self.heap[el_id], self.heap[element_id]
            element_id = el_id
            # print("heap loop", el_id)
    def del_min(self):
        heap = self.heap
        last_element = heap.pop()
        if not heap:
            return last_element
        item = heap[0]
        heap[0] = last_element
        self._heapify(0)
        return item
    # def min(self):
    #     if self.is_empty():
    #         return None
    #     return self.heap[0]
    def add(self, element):
        self.heap.append(element)
        self._inv_heapify (len (self.heap) - 1)
        # print(self.heap)