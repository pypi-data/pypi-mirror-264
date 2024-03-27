import pytest

from stlcontainers.priority_queue import PriorityQueue, PQEmptyError, PQSortError


@pytest.fixture
def max_heap():
    q = PriorityQueue([3, 1, 4, 5, 2])
    return q


@pytest.fixture
def min_heap():
    q = PriorityQueue([3, 1, 4, 5, 2], False)
    return q


@pytest.mark.parametrize(
    "e_to_push, expected_max_top, expected_min_top",
    [
        (6, 6, 1),
        (0, 5, 0),
        (1, 5, 1),
        (-1, 5, -1),
    ],
)
def test_push(max_heap, min_heap, e_to_push, expected_max_top, expected_min_top):
    sz = len(max_heap.arr)
    max_heap.push(e_to_push)
    assert expected_max_top == max_heap.top()
    assert max_heap.hs == sz + 1

    sz = len(min_heap.arr)
    min_heap.push(e_to_push)
    assert expected_min_top == min_heap.top()
    assert min_heap.hs == sz + 1


def test_pq_empty_error():
    q = PriorityQueue()
    with pytest.raises(PQEmptyError):
        q.pop()


@pytest.mark.parametrize(
    "e_to_push, expected_max_pop, expected_min_pop",
    [
        (6, 6, 1),
        (0, 5, 0),
        (1, 5, 1),
        (-1, 5, -1),
    ],
)
def test_pop(max_heap, min_heap, e_to_push, expected_max_pop, expected_min_pop):
    sz = len(max_heap.arr)
    max_heap.push(e_to_push)
    assert expected_max_pop == max_heap.pop()
    assert max_heap.hs == sz

    sz = len(min_heap.arr)
    min_heap.push(e_to_push)
    assert expected_min_pop == min_heap.pop()
    assert min_heap.hs == sz


def test_heap_sort(max_heap):
    max_heap.heap_sort()
    for i in range(1, len(max_heap.arr)):
        assert max_heap.arr[i] >= max_heap.arr[i - 1]


def test_heap_sort_error(min_heap):
    with pytest.raises(PQSortError):
        min_heap.heap_sort()
