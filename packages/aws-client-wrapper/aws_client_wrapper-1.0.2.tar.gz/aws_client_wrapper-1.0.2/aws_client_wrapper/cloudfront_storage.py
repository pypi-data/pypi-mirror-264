"""cloud_front_utility.py"""
import time
import logging
import traceback
from .connection import aws_cloudfront_client
from .utils import aws_client_response


@aws_cloudfront_client()
def _get_distribution_list(cloudfront_client=None):
    """This is for getting the distribution list"""
    try:
        response = cloudfront_client.list_distributions()
        return aws_client_response(response['DistributionList']['Items'], 200, None)
    except Exception as e:
        logging.error("Error in getting the distribution list: %s", e)
        logging.error(traceback.format_exc())
        return aws_client_response([], 500, str(e))

@aws_cloudfront_client()
def _invalidate_cloudfront(cloudfront_client=None, aws_distribution_id=None, invalidation_paths=None):
    """This is for invalidating the cloudfront"""
    try:
        response = cloudfront_client.create_invalidation(DistributionId=aws_distribution_id,
                                                                InvalidationBatch={'Paths': {'Quantity': len(invalidation_paths),
                                                                                            'Items': invalidation_paths},
                                                                                    'CallerReference': str(int(time.time())) 
                                                                                    })
        return aws_client_response(response, 200, None)
    except Exception as e:
        logging.error("Error in invalidating the cloudfront: %s", e)
        logging.error(traceback.format_exc())
        return aws_client_response(None, 500, str(e))

@aws_cloudfront_client()
def _get_invalidation_status(cloudfront_client=None, aws_distribution_id=None, invalidation_id=None):
    """This is for checking the invalidation status"""
    try:
        response = cloudfront_client.get_invalidation(DistributionId=aws_distribution_id, Id=invalidation_id)
        return aws_client_response(response['Invalidation']['Status'], 200, None)
    except Exception as e:
        logging.error("Error in getting the invalidation status: %s", e)
        logging.error(traceback.format_exc())
        return aws_client_response(None, 500, str(e))

