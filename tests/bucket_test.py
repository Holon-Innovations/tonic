import pytest
import random

from tonic import Tonic
from tonic.classes import *
from tonic.exceptions import *
from tests.config import Config

@pytest.fixture
def tonic():
    config_data = Config.get()["testing"]
    tonic = Tonic(endpoint=config_data["api_endpoint"], access_id=config_data["auth_token_id"], secret_key=config_data["auth_token_secret"])
    return tonic

def test_create_bucket(tonic):
    # create bucket using a random name
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    res = tonic.create_bucket(bucket_name)
    assert res["status_code"] == 200
    # get list of buckets (this returns a list of bucket objects)
    res = tonic.list_buckets()
    assert res["status_code"] == 200
    bucket_list = res["result"]
    # check if bucket exists
    assert isinstance(bucket_list, list)
    found = False
    for bucket in bucket_list:
        if bucket["name"] == bucket_name:
            found = True
            break
    assert found

def test_create_bucket_already_exists(tonic):
    # create bucket using a random name
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    # create bucket
    res = tonic.create_bucket(bucket_name)
    assert res["status_code"] == 200
    # create again
    res = tonic.create_bucket(bucket_name)
    assert res["status_code"] == 409

def test_list_buckets(tonic):
    # list buckets
    res = tonic.list_buckets()
    assert res["status_code"] == 200
    buckets = res["result"]
    assert isinstance(buckets, list)

def test_delete_bucket(tonic):
    # create bucket using a random name
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    res = tonic.create_bucket(bucket_name)
    assert res is not None
    # delete bucket
    res = tonic.delete_bucket(bucket_name)
    assert res is not None
    assert res["status_code"] == 200
    # get list buckets (this returns a list of bucket objects)
    res = tonic.list_buckets()
    assert res["status_code"] == 200
    buckets_list = res["result"]
    # check if bucket exists, it should not
    assert isinstance(buckets_list, list)
    for bucket in buckets_list:
        if bucket["name"] == bucket_name:
            assert False

def test_delete_bucket_doesnt_exist(tonic):
    # create bucket name
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    # delete bucket
    res = tonic.delete_bucket(bucket_name)
    assert res["status_code"] == 404

def test_delete_bucket_locked(tonic):
    # create bucket using a random name
    bucket_name = "s3-bucket-" + str(random.randint(1000, 9999))
    res = tonic.create_bucket(bucket=bucket_name, bucket_locked=True)
    assert res is not None
    # delete bucket
    res = tonic.delete_bucket(bucket_name)
    assert res["status_code"] == 403
    # get list buckets (this returns a list of bucket objects)
    res = tonic.list_buckets()
    assert res["status_code"] == 200
    bucket_list = res["result"]
    # check if bucket exists, it still should be there
    assert isinstance(bucket_list, list)
    found = False
    for bucket in bucket_list:
        if bucket["name"] == bucket_name:
            found = True
            break
    assert found