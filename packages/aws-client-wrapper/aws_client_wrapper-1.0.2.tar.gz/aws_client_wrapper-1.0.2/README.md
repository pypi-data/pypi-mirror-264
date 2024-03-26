**##AWS Client Wrapper**

**Overview**

aws-client-wrapper is a Python library designed to simplify  role base interactions with Amazon Web Services (AWS) resources using ARN this library is designed role based access for AWS resources from GCP serverless service like Cloud-Run, GAE. It provides a convenient wrapper around AWS SDK functionalities, focusing on operations related to AWS S3 buckets and AWS CloudFront.


**Features**

Support for AWS S3 bucket operations and AWS CloudFront cache operations.
Role-based access to AWS resources using ARN.
Compatibility with webapp2 and gunicorn apps.
Internal use of Redis cache to reduce fetching AWS temporary credentials repeatedly. Temporary credentials are stored in Redis cache for 3500 minutes.
Ability to insert API call operation stats into logs by passing a stats function name along with project_id, dataset_id, and table_id during configuration.

**Required ENV variable for working with aws resource**

1. set AWS_ROLE_ARN in the as ENV variable and key name should = AWS_ROLE_ARN (mandetory)
2. enable redis cache feature set REDIS_HOST as ENV variable and key name should = REDISHOST (optional)
3. enable to your gcp services to communicate with AWS



**Installation**

You can install aws-client-wrapper via pip:

```bash
pip install aws-client-wrapper
```

**Usage**

**Configuration**

Configure aws-client-wrapper in your application initialization file:

```python
from aws_client_wrapper import configure
configure(
    aws_stats_func=None, 
    aws_stats_project_id=None,
    aws_stats_dataset_id=None, 
    aws_stats_table_id=None
)
```
**Example Usage**

```python
# Importing AWS S3 and CloudFront clients

from aws_client_wrapper import s3_client, cloud_front

# Example usage of AWS S3 client functions
s3_client.get_data_from_s3(bucket_name=None, key=None)
s3_client.get_keys_object_by_prefix_from_s3(bucket_name=None, key=None)
s3_client.check_key_exist_from_s3(bucket_name=None, key=None)
s3_client.upload_data_to_s3(bucket_name=None, key=None, data=None, content_type=None,
                          acl=None, CacheControl=None)
s3_client.delete_data_from_s3(bucket_name=None, key=None)

# Example usage of AWS CloudFront client functions
cloud_front.invalidate_cloudfront(aws_distribution_id=None, invalidation_paths=None)
cloud_front.get_invalidation_status(aws_distribution_id=None, invalidation_id=None)
```
**Response Format**

The response format of each function will be in JSON format:

```json
{
    "data": "string"|"dict"|"list"| None,
    "status_code": 200,
    "error_message": ""
}
```
**License**

This project is licensed under the MIT License - see the LICENSE file for details.

**Support**
For any queries or issues, please [Contact Us](mailto:anilkumar.maurya@bluestacks.com)


