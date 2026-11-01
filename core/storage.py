from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StagingMediaStorage(S3Boto3Storage):
    """Read existing media while keeping staging writes in their own prefix."""

    file_overwrite = False

    def save(self, name, content, max_length=None):
        prefix = settings.R2_UPLOAD_PREFIX + '/'
        if not name.startswith(prefix):
            name = prefix + name.lstrip('/')
        return super().save(name, content, max_length=max_length)

    def delete(self, name):
        if name.startswith(settings.R2_UPLOAD_PREFIX + '/'):
            return super().delete(name)
