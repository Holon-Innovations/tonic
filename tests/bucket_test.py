import pytest
import random

from tonic import Tonic
from tonic.classes import *
from tonic.exceptions import *
from tests.config import config

@pytest.fixture
def tonic():
    config_data = config.get()["testing"]
    tonic = Tonic(endpoint=config_data["api_endpoint"], access_id=config_data["auth_token_id"], secret_key=config_data["auth_token_secret"])
    return tonic

def test_create_bucket(tonic):
    # create bucket using a random name
    bucket_name = "test-bucket-" + str(random.randint(1000, 9999))
    res = tonic.create_bucket(bucket_name)
    assert res is not None
    assert "created successfully" in res["message"]
    # get list buckets (this returns a list of bucket objects)
    buckets_list = tonic.list_buckets()
    # check if bucket exists
    assert isinstance(buckets_list, list)
    for bucket in buckets_list:
        if bucket.name == bucket_name:
            break
    else:
        assert False

def test_create_bucket_already_exists(tonic):
    # create bucket using a random name
    bucket_name = "test-bucket-" + str(random.randint(1000, 9999))
    try:
        # create bucket
        res = tonic.create_bucket(bucket_name)
        assert res is not None
        # create again
        res = tonic.create_bucket(bucket_name)
        # should not reach here
        assert False
    except PopBadResponse as e:
        assert e.response.status == 409

def test_list_buckets(tonic):
    # list buckets
    buckets = tonic.list_buckets()
    assert isinstance(buckets, list)
    print("\nResults ->")
    for bucket in buckets:
        print(bucket.name)
    print("--------------------")

def test_delete_bucket(tonic):
    # create bucket using a random name
    bucket_name = "test-bucket-" + str(random.randint(1000, 9999))
    res = tonic.create_bucket(bucket_name)
    assert res is not None
    # delete bucket
    res = tonic.delete_bucket(bucket_name)
    assert res is not None
    assert "deleted successfully" in res["message"]
    # get list buckets (this returns a list of bucket objects)
    buckets_list = tonic.list_buckets()
    # check if bucket exists, it should not
    assert isinstance(buckets_list, list)
    for bucket in buckets_list:
        if bucket.name == bucket_name:
            assert False

def test_delete_bucket_doesnt_exist(tonic):
    # create bucket name
    bucket_name = "test-bucket-" + str(random.randint(1000, 9999))
    # delete bucket
    try:
        res = tonic.delete_bucket(bucket_name)
        assert False
    except PopBadResponse as e:
        assert e.response.status == 404

def test_delete_bucket_locked(tonic):
    # create bucket using a random name
    bucket_name = "test-bucket-" + str(random.randint(1000, 9999))
    res = tonic.create_bucket(bucket=bucket_name, bucket_locked=True)
    assert res is not None
    # delete bucket
    try:
        res = tonic.delete_bucket(bucket_name)
        assert False
    except PopBadResponse as e:
        assert e.response.status == 403
    # get list buckets (this returns a list of bucket objects)
    buckets_list = tonic.list_buckets()
    # check if bucket exists, it still should be there
    assert isinstance(buckets_list, list)
    for bucket in buckets_list:
        if bucket.name == bucket_name:
            break
    else:
        assert False