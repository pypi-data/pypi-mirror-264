"""AWS wrapper utils"""
# from . import (aws_stats_func, aws_stats_project_id, aws_stats_dataset_id, aws_stats_table_id)

def insert_stats_into_bigquery(data: dict) -> None:
    """insert stats"""
    from .stats import AwsStats
    aws_stats = AwsStats()
    if aws_stats.get_func() and aws_stats.get_project_id() and aws_stats.get_dataset_id() and aws_stats.get_table_id():
        aws_stats.get_func()(aws_stats.get_project_id(), aws_stats.get_dataset_id(), aws_stats.get_table_id(), data)

def aws_client_response(data, status_code, error_message) -> dict:
    """return s3 client operation response object"""
    return {'data': data, 'status_code': status_code, 'error_message':error_message}
