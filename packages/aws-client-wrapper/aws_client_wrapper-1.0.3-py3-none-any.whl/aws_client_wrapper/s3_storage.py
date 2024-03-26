"""s3 bucket utility functions"""
import json
import logging
import traceback
from .connection import aws_s3_client
from .utils import aws_client_response

@aws_s3_client()
def _get_data_from_s3(s3_client=None, bucket_name=None, key=None):
    """Get data from S3."""
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        return aws_client_response(response['Body'].read().decode('utf-8'), 200, None)
    except s3_client.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            logging.error(f"Bucket '{bucket_name}' does not exist.")
        else:
            logging.error(f"Error accessing S3: {error_message}")
            logging.error(f"Object '{key}' does not exist in bucket '{bucket_name}'.")
        return aws_client_response(None, error_code, error_message)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error accessing S3: {e}")
        logging.error(f"Object '{key}' does not exist in bucket '{bucket_name}'.")
        return aws_client_response(None, 500, str(e))

@aws_s3_client()
def _get_keys_object_by_prefix_from_s3(s3_client=None, bucket_name=None, key=None, delimiter=None):
    """Get all keys with a given prefix from a bucket."""
    try:
        params = {'Bucket': bucket_name, 'Prefix': key}
        if delimiter:
            params['Delimiter'] = delimiter

        response_list = []
        while True:
            response = s3_client.list_objects_v2(**params)
            if 'CommonPrefixes' in response:
                # Prefixes if any
                response_list.extend([{'Key': obj['Prefix']} for obj in response['CommonPrefixes']])
            if 'Contents' in response:
                # Key: The name that you assign to an object. You use the object key to retrieve the object.
                # Size: Size in bytes of the object
                response_list.extend([{"Key": content["Key"], "Size": content["Size"], 'LastModified': content['LastModified']} for content in response['Contents']])
            # Check if there are more results to retrieve
            if not response['IsTruncated']:
                break # No more keys to fetch
            params['ContinuationToken'] = response['NextContinuationToken']
        return aws_client_response(response_list, 200, None)
    except s3_client.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            logging.error(f"Bucket '{bucket_name}' does not exist.")
        else:
            logging.error(f"Error accessing S3: {error_message}")
            logging.error(f"No objects with prefix '{key}' found in bucket '{bucket_name}'.")
        return aws_client_response([], error_code, error_message)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error accessing S3: {e}")
        logging.error(f"No objects with prefix '{key}' found in bucket '{bucket_name}'.")
        return aws_client_response([], 500, str(e))


@aws_s3_client()
def _get_all_keys_from_s3(s3_client=None, bucket_name=None, key=None, continuation_token=None):
    """Get all keys from a bucket using pagination.
       while calling this function again and again, pass the continuation_token before calling this function again check as following
       response['IsTruncated'] is False then no need to call this function again
    """
    try:
        params = {'Bucket': bucket_name, 'Prefix': key}
        if continuation_token:
            params['ContinuationToken'] = continuation_token
        response = s3_client.list_objects_v2(**params)
        return aws_client_response(response, 200, None)
    except s3_client.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            logging.error(f"Bucket '{bucket_name}' does not exist.")
        else:
            logging.error(f"Error accessing S3 bucket: {bucket_name} with error_message : {error_message}")
        return aws_client_response({}, error_code, error_message)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error accessing S3 bucket: {bucket_name} and error: {e}")
        return aws_client_response({}, 500, str(e))


@aws_s3_client()
def _check_key_exist_from_s3(s3_client=None, bucket_name=None, key=None):
    """Check if a key exists in a bucket."""
    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
        return aws_client_response(True, 200, None)
    except s3_client.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            logging.error(f"Key '{key}' does not exist in bucket '{bucket_name}'.")
        else:
            logging.error(f"Error accessing S3: {error_message}")
            logging.error(f"Key '{key}' does not exist in bucket '{bucket_name}'.")
        return aws_client_response(False, error_code, error_message)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error accessing S3: {e}")
        logging.debug(f"Key '{key}' does not exist in bucket '{bucket_name}'.")
        return aws_client_response(False, 500, str(e))


@aws_s3_client()
def _upload_data_to_s3(s3_client=None, bucket_name=None, key=None, data=None,
                      content_type=None, acl=None,
                      CacheControl=None):
    """Upload data to S3.
    Args:
        bucket_name (str): Name of the bucket.
        s3_object_path (str): Path of the object in S3.
        data (str): Data to be uploaded.
    """
    try:
        if not data:
            logging.error("No data to upload.")
            return
        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        params = {'Bucket': bucket_name,
                    'Key': key,
                    'Body': data}
        if content_type:
            params['ContentType'] = content_type
        if acl:
            params['ACL'] = acl
        if CacheControl:
            params['CacheControl'] = CacheControl
        #doc link : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_object.html
        s3_client.put_object(**params)
        logging.debug(f"Data uploaded to '{key}' in bucket '{bucket_name}'.")
        return aws_client_response(True, 200, None)
    except s3_client.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            logging.error(f"Bucket '{bucket_name}' does not exist.")
        else:
            logging.error(f"Error accessing S3: {error_message}")
            logging.error(f"bucket_name: {bucket_name}, s3_object_path: {key}")
        return aws_client_response(False, error_code, error_message)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error accessing S3: {e}")
        logging.error(f"bucket_name: {bucket_name}, s3_object_path: {key}")
        return aws_client_response(False, 500, str(e))

@aws_s3_client()
def _delete_data_from_s3(s3_client=None, bucket_name=None, key=None):
    """Delete data from S3."""
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=key)
        logging.debug(f"Data deleted from '{key}' in bucket '{bucket_name}'.")
        return aws_client_response(True, 200, None)
    except s3_client.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            logging.error(f"Bucket '{bucket_name}' does not exist.")
        else:
            logging.error(f"Error accessing S3: {error_message}")
            logging.error(f"Data '{key}' does not exist in bucket '{bucket_name}'.")
        return aws_client_response(False, error_code, error_message)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error accessing S3: {e}")
        logging.error(f"Data '{key}' does not exist in bucket '{bucket_name}'.")
        return aws_client_response(False, 500, str(e))

@aws_s3_client()
def _delete_keys_from_s3(s3_client=None, bucket_name=None, key=None):
    """Delete keys from S3."""
    try:
        objects = [{'Key': key} for key in key]
        s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': objects})
        logging.debug(f"Keys deleted from bucket '{bucket_name}'.")
        return aws_client_response(True, 200, None)
    except s3_client.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            logging.error(f"Bucket '{bucket_name}' does not exist.")
        else:
            logging.error(f"Error accessing S3: {error_message}")
            logging.error(f"No objects with keys '{key}' found in bucket '{bucket_name}'.")
        return aws_client_response(False, error_code, error_message)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error accessing S3: {e}")
        logging.error(f"No objects with keys '{key}' found in bucket '{bucket_name}'.")
        return aws_client_response(False, 500, str(e))

@aws_s3_client()
def _delete_keys_by_prefix_from_s3(s3_client=None, bucket_name=None, key=None):
    """Delete keys with a given prefix from S3."""
    try:
        keys = [obj['Key'] for obj in _get_keys_object_by_prefix_from_s3(bucket_name=bucket_name, key=key)]
        return _delete_keys_from_s3(bucket_name=bucket_name, key=keys)
    except s3_client.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            logging.error(f"Bucket '{bucket_name}' does not exist.")
        else:
            logging.error(f"Error accessing S3: {error_message}")
            logging.error(f"No objects with prefix '{key}' found in bucket '{bucket_name}'.")
        return aws_client_response(False, error_code, error_message)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error accessing S3: {e}")
        logging.error(f"No objects with prefix '{key}' found in bucket '{bucket_name}'.")
        return aws_client_response(False, 500, str(e))

@aws_s3_client()
def _copy_object_from_s3(s3_client=None, bucket_name=None, source_path=None, destination_path=None,
                preserve_acl=True, acl=None):
    """Copy an object from one bucket to another."""
    try:
        params = {'Bucket': bucket_name,
                  'CopySource': {'Bucket': bucket_name, 'Key': source_path},
                  'Key': destination_path}
        if acl:
            params['ACL'] = acl
            params['MetadataDirective'] = 'REPLACE'
        response = s3_client.copy_object(**params)
        try:
            if preserve_acl:
                acl_response = s3_client.get_object_acl(Bucket=bucket_name, Key=source_path)
                params = {'Bucket': bucket_name, 'Key': destination_path}
                params['AccessControlPolicy'] = {'Owner':acl_response['Owner'], 'Grants': acl_response['Grants']}
                s3_client.put_object_acl(**params)
        except:
            logging.error(traceback.format_exc())

        return aws_client_response(response, 200, None)
    except s3_client.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            logging.error(f"Bucket '{bucket_name}' does not exist.")
        else:
            logging.error(f"Error accessing S3: {error_message}")
            logging.error(f"Key '{source_path}' does not exist in bucket '{bucket_name}'.")
        return aws_client_response(None, error_code, error_message)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error accessing S3: {e}")
        logging.error(f"Key '{source_path}' does not exist in bucket '{bucket_name}'.")
        return aws_client_response(None, 500, str(e))



@aws_s3_client()
def _upload_content_from_file_to_s3(s3_client=None, bucket_name=None,
                            file=None, key=None,
                            content_type=None, acl=None,
                            CacheControl=None):
    """Upload content from a file to S3."""
    try:
        file.seek(0) #reset the file pointer to the beginning
        params = {'Bucket': bucket_name,
                    'Key': key,
                    'Body': file.read()}
        if content_type:
            params['ContentType'] = content_type
        if acl:
            params['ACL'] = acl
        if CacheControl:
            params['CacheControl'] = CacheControl
        s3_client.put_object(**params)
        logging.debug(f"Data uploaded to '{key}' in bucket '{bucket_name}'.")
        return aws_client_response(True, 200, None)
    except s3_client.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            logging.error(f"Bucket '{bucket_name}' does not exist.")
        else:
            logging.error(f"Error accessing S3: {error_message}")
            logging.error(f"bucket_name: {bucket_name}, s3_object_path: {key}")
        return aws_client_response(False, error_code, error_message)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error accessing S3: {e}")
        logging.error(f"bucket_name: {bucket_name}, s3_object_path: {key}")
        return aws_client_response(False, 500, str(e))

    
@aws_s3_client()
def _generate_presigned_url_from_s3(s3_client=None, bucket_name=None, key=None, expiration=3600):
    """generate presigned url for S3 object"""
    try:
        url = s3_client.generate_presigned_url('get_object',
                                              Params={'Bucket': bucket_name, 'Key': key},
                                              ExpiresIn=expiration)
        return aws_client_response(url, 200, None)
    except s3_client.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            logging.error(f"Bucket '{bucket_name}' does not exist.")
        else:
            logging.error(f"Error accessing S3: {error_code} and error: {error_message}")
        return aws_client_response(None, error_code, error_message)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error accessing S3: {e}")
    return aws_client_response(None, 500, str(e))

