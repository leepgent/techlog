# coding=utf-8
from __future__ import unicode_literals
from django.conf import settings

from storages.backends.s3boto import S3BotoStorage


class StaticRootS3BotoStorage(S3BotoStorage):
    def __init__(self):
        super(StaticRootS3BotoStorage, self).__init__()


class MediaRootS3BotoStorage(S3BotoStorage):
    def __init__(self):
        super(MediaRootS3BotoStorage, self).__init__(bucket=settings.AWS_MEDIA_BUCKET_NAME)
