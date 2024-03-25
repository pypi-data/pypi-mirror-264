# 1.0
* Features
    * Delete files - Delete any file inside the remote bucket
* Bugs
    * List files - Correct the none return, and now return a list

Example of use:
```
# imports
import s3simplemanager


s3 = S3SimpleManager(ssl_verification=False, bucket="s3_bucket_online", url="http://example.url.com/bucket", key_id="12345678", key_value="87654321")
s3.upload_files("example_path_local_file", "example_path_bucket_file")
for object in s3.list_files("example_path_bucket_file"):
    print(object)
```
