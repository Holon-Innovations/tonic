from enum import Enum

KB_SIZE = 1024
MB_SIZE = 1024 * KB_SIZE
GB_SIZE = 1024 * MB_SIZE
TB_SIZE = 1024 * GB_SIZE

MAX_MULTIPART_COUNT = 9999
MULTIPART_OBJECT_SIZE = 5 * MB_SIZE

class BUCKET_ACL(Enum):
    PRIVATE = "private"
    PUBLIC_READ = "public-read"
    PUBLIC_READ_WRITE = "public-read-write"
    AUTHENTICATED_READ = "authenticated-read"

class OBJECT_CHECKSUM_ALGORITHMS(Enum):
    CRC32 = "crc32"
    CRC32C = "crc32c"
    SHA1 = "sha1"
    SHA256 = "sha256"