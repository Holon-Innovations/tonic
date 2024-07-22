import math

from .types import *

def calc_object_parts(object_size: int) -> tuple[int, int, int]:
    """
    Calculate the part size, part count of an object.
    """
    if object_size <= 0:
        return 0, 0
    if object_size <= MULTIPART_OBJECT_SIZE:
        return object_size, 1
    part_size = MULTIPART_OBJECT_SIZE
    count = math.ceil(object_size / MULTIPART_OBJECT_SIZE)
    return part_size, count