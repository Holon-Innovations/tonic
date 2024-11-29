## Class: `Tonic`

### Constructor
`def __init__(self, endpoint: str, access_id: str | None = None, secret_key: str | None = None, region: str | None = None, http_client: urllib3.PoolManager | None = None, cert_check: bool = True):`

#### Parameters:
- `endpoint` (str): The API endpoint.
- `access_id` (str, optional): Access ID for authentication.
- `secret_key` (str, optional): Secret key for authentication.
- `region` (str, optional): Region specification.
- `http_client` (urllib3.PoolManager, optional): Custom HTTP client.
- `cert_check` (bool, optional): Enable/disable certificate checks. Default is `True`.

#### Example:
`tonic = Tonic(endpoint="https://api.example.com", access_id="my_access_id", secret_key="my_secret_key")`

### Response structure
The returning structure from each method in the API
- `status` The status of the call, either `success`, `error` or `warning`
- `status_code` The HTML status code for the call
- `result` The resulting data set for the call
- `result2` For certain calls, a second set of result data set can be returned
- `message` Any additional message from the call (generally used for errors and warnings)
### Methods

#### `client_response`
`def client_response(self, method: str, url: str, body: bytes | None = None, json: dict | None = None)`

Get a response from the server. This can be used to define your own methods.

##### Parameters:
- `method` (str): GET, POST, PUT or DELETE
- `url` (str): The url to call, this excludes the endpoint.
- `body` (bytes, optional): The bytes to be passed.
- `json` (bool, optional): The json to be passed.

##### Returns:
- `json`: Response from the server.

##### Example:
`response = tonic.client_response("GET", "/status?node_only=true")`

#### `create_bucket`
`def create_bucket(self, bucket: str, acl: BUCKET_ACL = BUCKET_ACL.PRIVATE, bucket_locked: bool = False) -> json:`

Creates a new bucket.

##### Parameters:
- `bucket` (str): Name of the bucket.
- `acl` (BUCKET_ACL, optional): Access control level. Default is `BUCKET_ACL.PRIVATE`.
- `bucket_locked` (bool, optional): Indicates if the bucket should be locked. Default is `False`.

##### Returns:
- `json`: Response from the server.

##### Example:
`response = tonic.create_bucket(bucket="my_bucket")`

#### `list_buckets`
`def list_buckets(self) -> list[Bucket]:`

Lists all buckets.

##### Returns:
- `list[Bucket]`: List of buckets.

##### Example:
`buckets = tonic.list_buckets()`

#### `delete_bucket`
`def delete_bucket(self, bucket: str) -> json:`

Deletes a bucket.

##### Parameters:
- `bucket` (str): Name of the bucket to delete.

##### Returns:
- `json`: Response from the server.

##### Example:
`response = tonic.delete_bucket(bucket="my_bucket")`

#### `put_object`
`def put_object(self, bucket: str, key: str, file: str | BinaryIO, content_type: str = "application/octet-stream", verify_sha256: bool = False) -> json:`

Uploads an object to a bucket.

##### Parameters:
- `bucket` (str): Name of the bucket.
- `key` (str): Key of the object.
- `file` (str | BinaryIO): File path or file data.
- `content_type` (str, optional): Content type of the object. Default is `"application/octet-stream"`.
- `verify_sha256` (bool, optional): Verify object checksum. Default is `False`.

##### Returns:
- `json`: Response from the server.

##### Example:
`response = tonic.put_object(bucket="my_bucket", key="my_object", file="path/to/file")`

#### `list_objects`
`def list_objects(self, bucket: str) -> list[Object]:`

Lists all objects in a bucket.

##### Parameters:
- `bucket` (str): Name of the bucket.

##### Returns:
- `list[Object]`: List of objects.

##### Example:
`objects = tonic.list_objects(bucket="my_bucket")`

#### `get_object_checksum`
`def get_object_checksum(self, bucket: str, key: str, algorithm: OBJECT_CHECKSUM_ALGORITHMS) -> str:`

Gets the checksum of an object.

##### Parameters:
- `bucket` (str): Name of the bucket.
- `key` (str): Key of the object.
- `algorithm` (OBJECT_CHECKSUM_ALGORITHMS): Checksum algorithm.

##### Returns:
- `str`: Object checksum.

##### Example:
`checksum = tonic.get_object_checksum(bucket="my_bucket", key="my_object", algorithm=OBJECT_CHECKSUM_ALGORITHMS.SHA256)`

#### `get_object`
`def get_object(self, bucket: str, key: str, file_path: str) -> json:`

Downloads an object to a specified file path.

##### Parameters:
- `bucket` (str): Name of the bucket.
- `key` (str): Key of the object.
- `file_path` (str): Path to save the downloaded object.

##### Returns:
- `json`: Response from the server.

##### Example:
`response = tonic.get_object(bucket="my_bucket", key="my_object", file_path="path/to/save")`

