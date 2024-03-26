from pathlib import Path
from typing import List

import boto3
import botocore


class S3Sync:
    """
    Class that holds the operations needed for synchronize local dirs to a given bucket.
    """

    def __init__(self, s3client):
        self._s3 = s3client

    def sync(self, bucket: str, prefix: str, dest: Path) -> [str]:
        """
        Sync source to dest, this means that all elements existing in
        source that not exists in dest will be copied to dest.

        No element will be deleted.

        :param bucket: bucket on S3.
        :param prefix: prefix to folder with files
        :param dest: Destination folder on local filesystem.

        :return: None
        """

        relative_paths = self.list_bucket_objects(bucket=bucket, prefix=prefix)
        # objects = self.list_local_objects(dest)

        for path in relative_paths:
            # Binary search.
            dest_path = Path(dest) / path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            self._s3.download_file(bucket, str(Path(prefix) / path), str(dest_path))

    def list_bucket_objects(self, bucket: str, prefix: str = None) -> [dict]:
        """
        List all objects for the given bucket.

        :param bucket: Bucket name.
        :param prefix: url for folder
        :return: A [dict] containing the elements in the bucket.

        Example of a single object.

        {
            'Key': 'example/example.txt',
            'LastModified': datetime.datetime(2019, 7, 4, 13, 50, 34, 893000, tzinfo=tzutc()),
            'ETag': '"b11564415be7f58435013b414a59ae5c"',
            'Size': 115280,
            'StorageClass': 'STANDARD',
            'Owner': {
                'DisplayName': 'webfile',
                'ID': '75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a'
            }
        }

        """
        files = []
        try:
            if prefix is not None:
                contents = self._s3.list_objects(Bucket=bucket, Prefix=prefix)['Contents']
            else:
                contents = self._s3.list_objects(Bucket=bucket)['Contents']
            for element in contents:
                key_string = Path(element["Key"])
                relative_path = key_string.relative_to(prefix)
                files.append(relative_path)
        except KeyError:
            # No Contents Key, empty bucket.
            return []
        else:
            return files

    @staticmethod
    def list_local_objects(folder: str) -> List[str]:
        """
        :param folder:  Root folder for resources you want to list.
        :return: A [str] containing relative names of the files.

        Example:

            /tmp
                - example
                    - file_1.txt
                    - some_folder
                        - file_2.txt

            >>> S3Sync.list_local_objects("/tmp/example")
            ['file_1.txt', 'some_folder/file_2.txt']

        """

        path = Path(folder)

        paths = []

        for file_path in path.rglob("*"):
            if file_path.is_dir():
                continue
            str_file_path = str(file_path)
            str_file_path = str_file_path.replace(f'{str(path)}/', "")
            paths.append(str_file_path)

        return paths
