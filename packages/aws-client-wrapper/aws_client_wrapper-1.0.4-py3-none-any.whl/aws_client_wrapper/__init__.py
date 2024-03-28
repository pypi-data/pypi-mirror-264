"""AWS resources wrapper"""
from .cloudfront import Cloudfront
from .s3 import S3Client
from .configure import configure
s3_client = S3Client()
cloud_front = Cloudfront()
