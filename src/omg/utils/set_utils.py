from typing import List


def _intersection(u: List, v: List) -> List:
    return list(set(u) & set(v))


def _intersection_is_empty(u: List, v: List) -> bool:
    return len(set(u).intersection(v)) == 0
