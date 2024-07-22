import pytest
import random
import zlib
import crc32c
import hashlib

from tonic import Tonic
from tonic.classes import *
from tonic.exceptions import *
from tests.config import config
from tonic.types import OBJECT_CHECKSUM_ALGORITHMS

@pytest.fixture
def tonic():
    config_data = config.get()["testing"]
    tonic = Tonic(endpoint=config_data["api_endpoint"], access_id=config_data["auth_token_id"], secret_key=config_data["auth_token_secret"])
    return tonic

def test_put_object_file(tonic):
    # create bucket using a random name
    bucket_name = "test-bucket-" + str(random.randint(1000, 9999))
    tonic.create_bucket(bucket_name)
    # put object
    res = tonic.put_object(
        bucket_name=bucket_name,
        object_name="test-file.txt",
        file="tests/random_files/text1.txt",
        content_type="text/plain",
        verify_sha256=True)
    print(f"\nresponse ->")
    print(res)

def test_put_object_file_as_bin(tonic):
    # create bucket using a random name
    bucket_name = "test-bucket-" + str(random.randint(1000, 9999))
    tonic.create_bucket(bucket_name)
    with open("tests/random_files/text1.txt", "rb") as file_data:
        # put object
        res = tonic.put_object(
            bucket_name=bucket_name,
            object_name="test-file.txt",
            file=file_data,
            content_type="text/plain",
            verify_sha256=True)
        print(f"\nresponse ->")
        print(res)

def test_put_large_object_file(tonic):
    # create bucket using a random name
    bucket_name = "test-bucket-" + str(random.randint(1000, 9999))
    tonic.create_bucket(bucket_name)
    # put object
    res = tonic.put_object(
        bucket_name=bucket_name,
        object_name="med-blob1.bin",
        file="tests/random_files/medblob1.bin")
    print(f"\nresponse ->")
    print(res)

def test_put_object_file_already_exists(tonic):
    # create bucket using a random name
    bucket_name = "test-bucket-" + str(random.randint(1000, 9999))
    tonic.create_bucket(bucket_name)
    # put object
    res = tonic.put_object(
        bucket_name=bucket_name,
        object_name="test-file.txt",
        file="tests/random_files/text1.txt",
        content_type="text/plain")
    try:
        # put object again
        res = tonic.put_object(
            bucket_name=bucket_name,
            object_name="test-file.txt",
            file="tests/random_files/text1.txt",
            content_type="text/plain")
        assert False
    except PopBadResponse as e:
        assert e.response.status == 409

def test_list_objects(tonic):
    # get buckets
    buckets = tonic.list_buckets()
    assert isinstance(buckets, list)

    # get objects for each bucket
    for bucket in buckets:
        objects = tonic.list_objects(bucket.name)
        assert isinstance(objects, list)
        print(f"\n{bucket.name} results ->")
        for object in objects:
            print(object.name)
        print("--------------------")

def test_get_crc32c(tonic):
    # calc local crc32
    crc32c_val = 0
    with open("tests/random_files/medblob1.bin", "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            crc32c_val = crc32c.crc32c(data, crc32c_val)
    local_crc32c = f"{crc32c_val & 0xFFFFFFFF:08x}"

    # create bucket using a random name
    bucket_name = "test-bucket-" + str(random.randint(1000, 9999))
    tonic.create_bucket(bucket_name)
    # put object
    res = tonic.put_object(
        bucket_name=bucket_name,
        object_name="med-blob1.bin",
        file="tests/random_files/medblob1.bin")
    # get crc32c
    res = tonic.get_object_checksum(bucket_name, "med-blob1.bin", OBJECT_CHECKSUM_ALGORITHMS.CRC32C)
    assert res is not None
    assert res["checksum"] == local_crc32c
    assert res["algorithm"] == "crc32c"
    print(f"\nchecksum -> {res['checksum']}")
    print(f"algorithm -> {res['algorithm']}")

def test_get_sha256(tonic):
    # calc local sha256
    sha256 = hashlib.sha256()
    with open("tests/random_files/medblob1.bin", "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)
    local_sha256 = sha256.hexdigest()

    # create bucket using a random name
    bucket_name = "test-bucket-" + str(random.randint(1000, 9999))
    tonic.create_bucket(bucket_name)
    # put object
    res = tonic.put_object(
        bucket_name=bucket_name,
        object_name="med-blob1.bin",
        file="tests/random_files/medblob1.bin")
    # get sha256
    res = tonic.get_object_checksum(bucket_name, "med-blob1.bin", OBJECT_CHECKSUM_ALGORITHMS.SHA256)
    assert res is not None
    assert res["checksum"] == local_sha256
    assert res["algorithm"] == "sha256"
    print(f"\nchecksum -> {res['checksum']}")
    print(f"algorithm -> {res['algorithm']}")