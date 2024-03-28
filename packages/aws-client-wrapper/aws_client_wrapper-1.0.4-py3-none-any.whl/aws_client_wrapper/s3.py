""""S3 client wrapper for AWS SDK."""
from . import s3_storage

class S3Client:
    """S3 client wrapper class"""
    def get_data_from_s3(self, bucket_name=None, key=None):
        """get data from s3"""
        return s3_storage._get_data_from_s3(bucket_name=bucket_name, key=key)

    def get_keys_object_by_prefix_from_s3(self, bucket_name=None, key=None):
        """get keys object by prefix from s3"""
        return s3_storage._get_keys_object_by_prefix_from_s3(bucket_name=bucket_name, key=key)

    def get_all_keys_from_s3(self, bucket_name=None, key=None, continuation_token=None):
        """get all keys from s3"""
        return s3_storage._get_all_keys_from_s3(bucket_name=bucket_name, key=key, continuation_token=continuation_token)

    def check_key_exist_from_s3(self, bucket_name=None, key=None):
        """check key exist from s3"""
        return s3_storage._check_key_exist_from_s3(bucket_name=bucket_name, key=key)

    def upload_data_to_s3(self, bucket_name=None, key=None, data=None, content_type=None,
                          acl=None, CacheControl=None):
        """upload data to s3"""
        return s3_storage._upload_data_to_s3(bucket_name=bucket_name, key=key, data=data,
                                             content_type=content_type, acl=acl, CacheControl=CacheControl)

    def upload_content_from_file_to_s3(self, bucket_name=None, key=None, file=None, content_type=None,
                                       acl=None, CacheControl=None):
        """upload content from file to s3"""
        return s3_storage._upload_content_from_file_to_s3(bucket_name=bucket_name, key=key,
                                                          file=file, content_type=content_type, acl=acl,
                                                          CacheControl=CacheControl)

    def copy_object_from_s3(self, bucket_name=None, destination_bucket_name=None, destination_key=None,
                            preserve_acl=False, acl=None):
        """copy object from s3"""
        return s3_storage._copy_object_from_s3(bucket_name=bucket_name,
                                              destination_bucket_name=destination_bucket_name,
                                              destination_key=destination_key, preserve_acl=preserve_acl, acl=acl)

    def delete_data_from_s3(self, bucket_name=None, key=None):
        """delete data from s3"""
        return s3_storage._delete_data_from_s3(bucket_name=bucket_name, key=key)

    def delete_keys_from_s3(self, bucket_name=None, key=None):
        """delete objects from s3
        :param bucket_name: bucket name
        :param key: list of keys
        """
        return s3_storage._delete_keys_from_s3(bucket_name=bucket_name, key=key)

    def delete_keys_by_prefix_from_s3(self, bucket_name=None, key=None):
        """delete objects by prefix from s3"""
        return s3_storage._delete_keys_by_prefix_from_s3(bucket_name=bucket_name, key=key)

    def generate_presigned_url_from_s3(self, bucket_name=None, key=None, expiration=3600):
        """generate presigned url from s3"""
        return s3_storage._generate_presigned_url_from_s3(bucket_name=bucket_name, key=key, expiration=expiration)
