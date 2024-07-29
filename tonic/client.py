from email import message
import os
import json
import re
from unittest import result
import urllib3
from typing import BinaryIO

from .classes import *
from .helpers import *
from .types import *
from .exceptions import *

API_ROOT = "/s3/v1"

class Tonic:
    def __init__(self,
        endpoint: str,
        access_id: str | None = None,
        secret_key: str | None = None,
        region: str | None = None,
        http_client: urllib3.PoolManager | None = None,
        cert_check: bool = True):

        # init
        self._endpoint = endpoint
        self._access_id = access_id
        self._secret_key = secret_key
        self._region = region
        self._http_client = http_client
        self._cert_check = cert_check

        # define headers
        headers = {
            'accept': 'application/json',
            'pop-app-key': '{"id": "' + self._access_id + '", "token": "' + self._secret_key + '"}',
            'Content-Type': 'application/json'
        }

        # get client
        self._http_client = urllib3.PoolManager(headers=headers, cert_reqs='CERT_REQUIRED' if self._cert_check else 'CERT_NONE')

    def __get_region(self):
        pass

    def __get_response(self, method: str, url: str, body: bytes | None = None, json: dict | None = None):
        # build url
        region = self.__get_region()
        if region is None:
            s3_url = f"{self._endpoint}/{API_ROOT}/{url}"
        else:
            s3_url = f"{region}-{self._endpoint}/{API_ROOT}/{url}"

        # make sure url is clean
        s3_url = s3_url.replace("://", ":/_/_").replace("//", "/").replace(":/_/_", "://")

        # get response
        response = self._http_client.request(
            method=method,
            url=s3_url,
            body=body,
            json=json,
            assert_same_host=True,
            timeout=urllib3.Timeout(connect=10.0, read=10.0),
            #timeout=urllib3.Timeout(connect=999.0, read=999.0),
            retries=urllib3.Retry(3)
        )

        # check response
        if response.status != 200:
            raise PopBadResponse(response)
        return response

    def create_bucket(self, bucket: str, acl: BUCKET_ACL = BUCKET_ACL.PRIVATE, bucket_locked: bool = False) -> json:
        response = self.__get_response(
            method="POST",
            url=f"/buckets/create-bucket/{bucket}",
            json={"acl": acl.value, "locked": bucket_locked}
            )
        return response.json()

    def list_buckets(self)-> list[Bucket]:
        response = self.__get_response(
            method="GET",
            url="/buckets/list-buckets"
            )
        res = response.json()
        result = []
        for bucket in res["buckets"]:
            result.append(Bucket(name=bucket["name"], creation_date=bucket["created"]))
        return result

    def delete_bucket(self, bucket: str) -> json:
        response = self.__get_response(
            method="DELETE",
            url=f"/buckets/delete-bucket/{bucket}"
            )
        return response.json()

    def __put_object_multipart(self,
        bucket: str,
        key: str,
        data: BinaryIO,
        length: int,
        content_type: str = "application/octet-stream",
        verify_sha256: bool = False
    ) -> json:

        # get the part size and count
        part_size, part_count = calc_object_parts(length)
        uploaded = 0
        which_part = 0
        upload_id = None

        # create the multipart object
        response = self.__get_response(
            method="POST",
            url=f"/objects/create-multipart-object/{bucket}/{key}",
            json={"part_count": part_count, "object_size": length, "content_type": content_type}
        )
        upload_id = response.json()["id"]

        # loop for each part
        while which_part < part_count:
            part_data = data.read(part_size)
            upload_size = len(part_data)
            uploaded += len(part_data)

            # upload the part
            response = self.__get_response(
                method="PUT",
                url=f"/objects/upload-object-part/{upload_id}/{which_part}/{upload_size}",
                body=part_data
            )
            which_part += 1

        # verify the file state by returning the object sha256
        if verify_sha256:
            response = self.__get_response(
                method="GET",
                url=f"/objects/get-object-checksum/sha256/{bucket}/{key}"
                )
            sha256 = response.json()["checksum"]
        else:
            sha256 = None
        return {
            "message": "Object uploaded successfully",
            "sha256": sha256
        }

    def put_object(self,
        bucket: str,
        key: str,
        file: any = str | BinaryIO,
        content_type: str = "application/octet-stream",
        verify_sha256: bool = False
    ) -> json:

        # check if file is a string, then it's a file path... otherwise it's a file data
        file_path = None
        file_data = None
        if isinstance(file, str):
            file_path = file
        else:
            file_data = file

        if file_path is not None:
            # make sure file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File '{file_path}' not found")

            # get file size
            file_size = os.stat(file_path).st_size

            # open the file and upload it
            with open(file_path, "rb") as file_data:
                result = self.__put_object_multipart(
                    bucket=bucket,
                    key=key,
                    data=file_data,
                    length=file_size,
                    content_type=content_type,
                    verify_sha256=verify_sha256
                )
        elif file_data is not None:
            # get file data
            file_data.seek(0, os.SEEK_END)
            file_size = file_data.tell()
            file_data.seek(0)

            # upload the file
            result = self.__put_object_multipart(
                bucket=bucket,
                key=key,
                data=file_data,
                length=file_size,
                content_type=content_type,
                verify_sha256=verify_sha256
            )
        else:
            raise ValueError("File path or file data is required")

        return result

    def list_objects(self, bucket: str) -> list[Object]:
        response = self.__get_response(
            method="GET",
            url=f"/objects/list-objects/{bucket}"
            )
        res = response.json()
        result = []
        for obj in res["objects"]:
            result.append(Object(name=obj["name"], creation_date=obj["created"]))
        return result

    def get_object_checksum(self, bucket: str, key: str, algorithm: OBJECT_CHECKSUM_ALGORITHMS) -> str:
        response = self.__get_response(
            method="GET",
            url=f"/objects/get-object-checksum/{algorithm.value}/{bucket}/{key}"
            )
        return response.json()

    def get_object(self, bucket: str, key: str, file_path: str) -> json:
        response = self.__get_response(
            method="GET",
            url=f"/objects/get-object-data/{bucket}/{key}"
            )
        with open(file_path, "wb") as file:
            file.write(response.data)

        return {
            "message": "Object downloaded successfully",
        }
