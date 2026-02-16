"""
Custom storage backends for S3 storage configuration.
"""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Custom storage for static files in S3.
    """
    def __init__(self, *args, **kwargs):
        # Set location based on AWS_LOCATION setting
        base_location = getattr(settings, 'AWS_LOCATION', '')
        if base_location:
            self.location = f'{base_location.rstrip("/")}/static'
        else:
            self.location = 'static'
        super().__init__(*args, **kwargs)


class MediaStorage(S3Boto3Storage):
    """
    Custom storage for media files in S3.
    """
    file_overwrite = False
    
    def __init__(self, *args, **kwargs):
        # Set location based on AWS_LOCATION setting
        base_location = getattr(settings, 'AWS_LOCATION', '')
        if base_location:
            self.location = f'{base_location.rstrip("/")}/media'
        else:
            self.location = 'media'
        super().__init__(*args, **kwargs)

