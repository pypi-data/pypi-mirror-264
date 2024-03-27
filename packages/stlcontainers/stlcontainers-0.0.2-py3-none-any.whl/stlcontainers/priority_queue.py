class PriorityQueue:
    def __init__(self, arr=[], is_max_heap=True) -> None:
        self.arr = arr
        self.hs = len(arr)
        self.is_max_heap = is_max_heap
        self.__build_heap()

    def __compare_should_on_top(self, lhs, rhs):
        """Compare given elements lhs & rhs.
        Return True if lhs should on be on top of rhs, as in heap.
        """
        if self.is_max_heap:
            return lhs > rhs
        else:
            return lhs < rhs

    def __heapify(self, i: int):
        """Assume sub-nodes of i are all valid heaps.
        Compare i with left & right children, swap and continue downwards.
        """
        idx = i
        l, r = idx * 2 + 1, idx * 2 + 2
        if l < self.hs and self.__compare_should_on_top(self.arr[l], self.arr[idx]):
            idx = l
        if r < self.hs and self.__compare_should_on_top(self.arr[r], self.arr[idx]):
            idx = r
        if idx != i:
            self.arr[i], self.arr[idx] = self.arr[idx], self.arr[i]
            self.__heapify(idx)

    def __build_heap(self):
        """Obvisously, for 0-indexed arr tree, [n/2...n) are leaf nodes.
        Iterate non-leaf nodes from bottom to top and heapify.
        """
        for i in range(self.hs // 2 - 1, -1, -1):
            self.__heapify(i)

    def __update_key(self, i: int, e):
        """Update self.arr[i]  to be value of given e.
        For max-heap, the update can only be 'increase';
        Similar for min-heap, the update can only be 'decrease'.
        """
        self.arr[i] = e
        while i and self.__compare_should_on_top(self.arr[i], self.arr[i // 2]):
            self.arr[i // 2], self.arr[i] = self.arr[i], self.arr[i // 2]
            i //= 2

    def heap_sort(self):
        """Heap sort self.arr; note that heap size will become zero."""
        if not self.is_max_heap:
            raise PQSortError()
        while self.hs:
            self.arr[0], self.arr[self.hs - 1] = self.arr[self.hs - 1], self.arr[0]
            self.hs -= 1
            self.__heapify(0)

    def top(self):
        if self.hs <= 0:
            raise PQEmptyError()
        return self.arr[0]

    def pop(self):
        res = self.top()
        self.arr[0], self.arr[self.hs - 1] = self.arr[self.hs - 1], self.arr[0]
        self.hs -= 1
        self.__heapify(0)
        return res

    def push(self, e):
        if self.hs < len(self.arr):
            self.arr[self.hs] = -float("inf")
        else:
            self.arr.append(-float("inf"))
        self.hs += 1
        self.__update_key(self.hs - 1, e)


class PQEmptyError(Exception):
    def __init__(self) -> None:
        super().__init__("Priority Queue is empty.")


class PQSortError(Exception):
    def __init__(self) -> None:
        super().__init__("Sort is not supported for min heap.")


if __name__ == "__main__":
    q = PriorityQueue([3, 1, 2, 3, 4])
    print("PQ:", q.arr)
    q.push(10)
    print("PQ:", q.arr)
