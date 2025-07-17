import time
from typing import List, Tuple

def selection_sort(arr: List[int]) -> Tuple[List[int], float]:
    """Implementação otimizada do Selection Sort"""
    arr = arr.copy()
    start_time = time.perf_counter()
    
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if i != min_idx:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr, time.perf_counter() - start_time

def insertion_sort(arr: List[int]) -> Tuple[List[int], float]:
    """Implementação otimizada do Insertion Sort"""
    arr = arr.copy()
    start_time = time.perf_counter()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    
    return arr, time.perf_counter() - start_time
