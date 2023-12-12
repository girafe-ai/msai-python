from typing import List


def binary_search(arr: List[int], target: int) -> bool:
    """binary_search

    Args:
        arr (List[int]): _description_
        target (int): _description_

    Returns:
        bool: result
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False
