import pytest
import os
import random
import crc32c
import hashlib

from tonic import Tonic
from tonic.classes import *
from tonic.exceptions import *
from tests.config import Config
from tonic.types import OBJECT_CHECKSUM_ALGORITHMS

@pytest.fixture
def tonic():
    config_data = Config.get()["testing"]
    tonic = Tonic(endpoint=config_data["api_endpoint"], access_id=config_data["auth_token_id"], secret_key=config_data["auth_token_secret"])
    return tonic

def test_put_object_file(tonic):
    # create bucket using a random name
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    res = tonic.create_bucket(bucket_name)
    assert res["status_code"] == 200
    # put object
    res = tonic.put_object(
        bucket=bucket_name,
        key="test-file.txt",
        file="tests/random_files/text1.txt",
        content_type="text/plain",
        verify_sha256=True)
    assert res["status_code"] == 200
    # get list of objects
    res = tonic.list_objects(bucket_name)
    assert res["status_code"] == 200
    object_list = res["result"]
    # check if object exists
    assert isinstance(object_list, list)
    found = False
    for obj in object_list:
        if obj["name"] == "test-file.txt":
            found = True
            break
    assert found

def test_put_object_file_as_bin(tonic):
    # create bucket using a random name
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    tonic.create_bucket(bucket_name)
    with open("tests/random_files/text1.txt", "rb") as file_data:
        # put object
        res = tonic.put_object(
            bucket=bucket_name,
            key="test-file.txt",
            file=file_data,
            content_type="text/plain",
            verify_sha256=True)
        print(f"\nresponse ->")
        print(res)

def test_put_large_object_file(tonic):
    # create bucket using a random name
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    tonic.create_bucket(bucket_name)
    # put object
    res = tonic.put_object(
        bucket=bucket_name,
        key="med-blob1.bin",
        file="tests/random_files/medblob1.bin")
    print(f"\nresponse ->")
    print(res)

def test_put_object_file_already_exists(tonic):
    # create bucket using a random name
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    res = tonic.create_bucket(bucket_name)
    assert res["status_code"] == 200
    # put object
    res = tonic.put_object(
        bucket=bucket_name,
        key="test-file.txt",
        file="tests/random_files/text1.txt",
        content_type="text/plain")
    assert res["status_code"] == 200
    # put object again
    res = tonic.put_object(
        bucket=bucket_name,
        key="test-file.txt",
        file="tests/random_files/text1.txt",
        content_type="text/plain")
    assert res["status_code"] == 409

def test_list_objects(tonic):
    # get buckets
    res = tonic.list_buckets()
    assert res["status_code"] == 200
    bucket_list = res["result"]
    assert isinstance(bucket_list, list)
    # get objects for each bucket
    for bucket in bucket_list:
        res = tonic.list_objects(bucket["name"])
        assert res["status_code"] == 200
        object_list = res["result"]
        assert isinstance(object_list, list)
        # stop if any objects is found
        if len(object_list) > 0:
            break

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
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    res = tonic.create_bucket(bucket_name)
    assert res["status_code"] == 200
    # put object
    res = tonic.put_object(
        bucket=bucket_name,
        key="med-blob1.bin",
        file="tests/random_files/medblob1.bin")
    # get crc32c
    res = tonic.get_object_checksum(bucket_name, "med-blob1.bin", OBJECT_CHECKSUM_ALGORITHMS.CRC32C)
    assert res["status_code"] == 200
    assert res["result"] == local_crc32c

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
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    tonic.create_bucket(bucket_name)
    # put object
    res = tonic.put_object(
        bucket=bucket_name,
        key="med-blob1.bin",
        file="tests/random_files/medblob1.bin")
    # get sha256
    res = tonic.get_object_checksum(bucket_name, "med-blob1.bin", OBJECT_CHECKSUM_ALGORITHMS.SHA256)
    assert res["status_code"] == 200
    assert res["result"] == local_sha256

def test_get_object(tonic):
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
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    res = tonic.create_bucket(bucket_name)
    assert res["status_code"] == 200
    # put object
    res = tonic.put_object(
        bucket=bucket_name,
        key="med-blob1.bin",
        file="tests/random_files/medblob1.bin")
    assert res["status_code"] == 200\
    # create a folder to save the object
    os.mkdir(f"tests/random_files/{bucket_name}")
    # get object
    res = tonic.get_object(bucket_name, "med-blob1.bin", f"tests/random_files/{bucket_name}/medblob1.bin")
    assert res["status_code"] == 200
    # calc local sha256 on returned file
    sha256 = hashlib.sha256()
    with open(f"tests/random_files/{bucket_name}/medblob1.bin", "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)
    local2_sha256 = sha256.hexdigest()
    assert local_sha256 == local2_sha256
    # delete all folders starting with "s3-bucket-"
    for folder in os.listdir("tests/random_files"):
        if folder.startswith("s3-bucket-"):
            # remove dir even if not empty
            os.system(f"rm -rf tests/random_files/{folder}")
