from unittest.mock import patch

from django.test import SimpleTestCase, override_settings
from storages.backends.s3boto3 import S3Boto3Storage

from .storage import StagingMediaStorage


@override_settings(R2_UPLOAD_PREFIX='staging/rfdocker')
class StagingMediaStorageTests(SimpleTestCase):
    def setUp(self):
        self.storage = StagingMediaStorage()

    def test_uploads_are_scoped_and_do_not_overwrite(self):
        with patch.object(S3Boto3Storage, 'save', return_value='saved') as save:
            content = object()
            self.storage.save('images/sample.jpg', content)
            save.assert_called_once_with(
                'staging/rfdocker/images/sample.jpg', content, max_length=None
            )
        self.assertFalse(self.storage.file_overwrite)

    def test_retry_does_not_duplicate_prefix(self):
        with patch.object(S3Boto3Storage, 'save') as save:
            content = object()
            self.storage.save('staging/rfdocker/images/sample.jpg', content)
            save.assert_called_once_with(
                'staging/rfdocker/images/sample.jpg', content, max_length=None
            )

    def test_production_media_cannot_be_deleted(self):
        with patch.object(S3Boto3Storage, 'delete') as delete:
            self.storage.delete('images/production.jpg')
            delete.assert_not_called()
            self.storage.delete('staging/rfdocker/images/sample.jpg')
            delete.assert_called_once_with('staging/rfdocker/images/sample.jpg')
