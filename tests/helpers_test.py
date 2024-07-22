import pytest
from tests.config import config
from tonic.helpers import *
from tonic.types import *

def test_calc_parts():
    size = 500
    part_size, part_count = calc_object_parts(size)
    assert part_size == 500
    assert part_count == 1
    size = MULTIPART_OBJECT_SIZE
    part_size, part_count = calc_object_parts(size)
    assert part_size == MULTIPART_OBJECT_SIZE
    assert part_count == 1
    size = MULTIPART_OBJECT_SIZE + 1
    part_size, part_count = calc_object_parts(size)
    assert part_size == MULTIPART_OBJECT_SIZE
    assert part_count == 2
    size = (MULTIPART_OBJECT_SIZE * 5) + 555
    part_size, part_count = calc_object_parts(size)
    assert part_size == MULTIPART_OBJECT_SIZE
    assert part_count == 6
