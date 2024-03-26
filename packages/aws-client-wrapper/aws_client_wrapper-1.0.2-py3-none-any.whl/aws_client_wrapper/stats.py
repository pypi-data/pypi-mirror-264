"""stats module"""
import threading

class AwsStats:
    """AwsStats class"""
    _instance = None
    _lock = threading.Lock()  # Create a lock object

    def set(self, aws_stats_func=None, aws_stats_project_id=None, aws_stats_dataset_id=None, aws_stats_table_id=None):
        self.aws_stats_func = aws_stats_func
        self.aws_stats_project_id = aws_stats_project_id
        self.aws_stats_dataset_id = aws_stats_dataset_id
        self.aws_stats_table_id = aws_stats_table_id

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def get_func(self):
        """get function"""
        return self.aws_stats_func

    def get_project_id(self):
        """get project id"""
        return self.aws_stats_project_id

    def get_dataset_id(self):
        """get dataset id"""
        return self.aws_stats_dataset_id

    def get_table_id(self):
        """get table id"""
        return self.aws_stats_table_id
