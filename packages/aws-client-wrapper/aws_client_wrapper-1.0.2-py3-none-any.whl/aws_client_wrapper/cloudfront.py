"""cloudfront wrapper"""
from . import cloudfront_storage

class Cloudfront:
    """Cloudfront wrapper class"""	
    def get_distribution_list(self):
        """get distribution list"""
        return cloudfront_storage._get_distribution_list()

    def invalidate_cloudfront(self, aws_distribution_id=None, invalidation_paths=None):
        """invalidate cloudfront"""
        return cloudfront_storage._invalidate_cloudfront(aws_distribution_id=aws_distribution_id,
                                                         invalidation_paths=invalidation_paths)

    def get_invalidation_status(self, aws_distribution_id=None, invalidation_id=None):
        """get invalidation status"""
        return cloudfront_storage._get_invalidation_status(aws_distribution_id=aws_distribution_id,
                                                           invalidation_id=invalidation_id)
