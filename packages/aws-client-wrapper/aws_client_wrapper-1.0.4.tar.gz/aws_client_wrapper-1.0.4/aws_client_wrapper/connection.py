"""This is for getting the base connection for the AWS role"""
import logging
import datetime
import os
import time
import json
from functools import wraps
import requests
import boto3
from . import utils, constants
from .CacheService import REDIS_WRAPPER


def get_token():
        """"This is for getting the metadata from the GCP instance"""
        metadata_url = f'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?format=standard&audience=gcp'
        headers = {'Metadata-Flavor': 'Google'}
        try:
            meta_request = requests.get(metadata_url, headers=headers, timeout=60)
            meta_request.raise_for_status()
            return meta_request.text # this token is valid for 1 hour as per docs
        except requests.exceptions.RequestException as e:
            raise Exception(f'Compute Engine token error: {e}') from e


def get_sts_credentials(duration_seconds:int):
    """Returns a set of temporary security credentials from Security Token Service"""
    try:
        if REDIS_WRAPPER:
            credentials = REDIS_WRAPPER.get(constants.REDIS_KEY)
            if credentials:
                logging.debug("sts_credentials_is_found_in_cache")
                return json.loads(credentials)
        sts_client = boto3.client('sts', aws_access_key_id='', aws_secret_access_key='')
        timestamp = int(time.time())
        session_name = f"session_{timestamp}"
        res = sts_client.assume_role_with_web_identity(
        RoleArn=os.environ['AWS_ROLE_ARN'],
        WebIdentityToken=get_token(),
        RoleSessionName=session_name,
        DurationSeconds=duration_seconds
        )
        credentials = {
        'AccessKeyId': res['Credentials']['AccessKeyId'],
        'SecretAccessKey': res['Credentials']['SecretAccessKey'],
        'SessionToken': res['Credentials']['SessionToken']
        }
        if REDIS_WRAPPER:
            REDIS_WRAPPER.set(constants.REDIS_KEY, json.dumps(credentials), min(duration_seconds, constants.REDIS_TIMEOUT))
        return credentials
    except Exception as e:
        raise Exception(f'get_sts_credentials error: {e}') from e


def insert_s3_operation_stats_into_bq(called_by, bucket_name, prefix):
    """insert stats into BQ"""
    try:
        url = os.environ.get('HTTP_HOST')
        uri = os.environ.get('RAW_URI') or os.environ.get('PATH_INFO')
        data = {
            "json": {
                "bucket_name": bucket_name,
                "api": f"{url}{uri}",
                "directory_prefix": prefix,
                "called_by": called_by,
                "created_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        utils.insert_stats_into_bigquery(data)
    except Exception as e:
        logging.error(e)


def aws_s3_client(duration_seconds: int=3600):
    """aws_s3_client decorator"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                bucket_name = kwargs.get('bucket_name')
                key = kwargs.get('key')
                source_path = kwargs.get('source_path')
                destination_path = kwargs.get('destination_path')
                if source_path and destination_path:
                    key = f"from_key: {source_path} to to_path: {destination_path}"
                if isinstance(key, list):
                    key = ",".join(key)

                if not bucket_name:
                    raise Exception("aws_s3_client: bucket_name not found in args or kwargs")
                logging.debug(f"aws_s3_client: bucket_name={bucket_name}")
                credentials = get_sts_credentials(duration_seconds)
                s3_client = boto3.client('s3', aws_access_key_id=credentials['AccessKeyId'],
                                     aws_secret_access_key=credentials['SecretAccessKey'],
                                     aws_session_token=credentials['SessionToken'])
                #insert stats into BQ
                insert_s3_operation_stats_into_bq(func.__name__, bucket_name, key)
                return func(s3_client=s3_client, *args, **kwargs)
            except Exception as e:
                raise Exception(f'aws_s3_client error: {e}') from e
        return wrapper
    return decorator


def aws_cloudfront_client(duration_seconds: int=3600):
    """aws_cloudfront_client decorator"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                credentials = get_sts_credentials(duration_seconds)
                cloudfront_client = boto3.client('cloudfront', aws_access_key_id=credentials['AccessKeyId'],
                                              aws_secret_access_key=credentials['SecretAccessKey'],
                                              aws_session_token=credentials['SessionToken'],
                                              verify=False)
                #insert stats into BQ
                aws_distribution_id = kwargs.get('aws_distribution_id')
                invalidation_paths = kwargs.get('invalidation_paths') or kwargs.get('invalidation_id')
                insert_s3_operation_stats_into_bq(func.__name__, aws_distribution_id, invalidation_paths)
                return func(cloudfront_client=cloudfront_client, *args, **kwargs)
            except Exception as e:
                raise Exception(f'aws_cloudfront_client error: {e}') from e
        return wrapper
    return decorator
