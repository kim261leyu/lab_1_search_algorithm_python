

class IndexedHeap:
    def __init__(self):
        self.heap = []  
        self.position = {}
        
    def push(self, row, col, count):
        self.heap.append((count, row, col));
        index = len(self.heap) - 1;
        self.position[(row, col)] = index;
        
        self._sift_up(index);
        
    def _sift_up(self, i):
        while i > 0 and self.heap[i][0] < self.heap[self._parent(i)][0]:
            self._swap(i, self._parent(i));
            i = self._parent(i)
        
    def _parent(self, i):
        return (i - 1) // 2;
        
    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i];
        self.position[(self.heap[i][1], self.heap[i][2])] = i;
        self.position[(self.heap[j][1], self.heap[j][2])] = j;
        
    def _left(self, i):
        return i * 2 + 1;
        
    def _right(self, i):
        return i * 2 + 2;
        
    def _sift_down(self, i):
        while True:
            left = self._left(i)
            right = self._right(i)
            smallest = i

            if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest == i:
                break

            self._swap(i, smallest)
            i = smallest
            
    def pop_min(self):
        result = self.heap[0];
        self.delete(result[1], result[2])
            
        return result;
        
    def peek_min(self):
        return self.heap[0];
        
        
    def update(self, row, col, new_count):
        i = self.position[(row, col)]
        old_count = self.heap[i][0]
        self.heap[i] = (new_count, row, col)
        
        if new_count < old_count:
            self._sift_up(i);
        elif new_count > old_count:
            self._sift_down(i);
            
    def delete(self, row, col):
        index = self.position[(row, col)];
        self._swap(index, len(self.heap) - 1);
        self.heap.pop();
        del self.position[(row, col)];
        if index < len(self.heap):
            if self.heap:
                self._sift_down(index);
            if self.heap[index][0] < self.heap[self._parent(index)][0]:
                self._sift_up(index);
            
            
    
        