import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# R2 configuration from environment variables
R2_ENDPOINT_URL = os.getenv('R2_ENDPOINT_URL')
AWS_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
BUCKET_NAME = os.getenv('R2_BUCKET_NAME')

# Configure S3 client for R2 with auto region
s3 = boto3.client('s3',
    endpoint_url=R2_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=Config(
        signature_version='s3v4',
        region_name='auto'  # Use 'auto' for R2
    ),
)

def upload_directory(local_directory, bucket, prefix=""):
    """Upload a directory to R2"""
    for root, dirs, files in os.walk(local_directory):
        for filename in files:
            # Construct the full local path
            local_path = os.path.join(root, filename)
            
            # Construct the R2 path
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join(prefix, relative_path).replace("\\", "/")
            
            # Determine content type
            content_type = 'image/png' if filename.endswith('.png') else 'application/octet-stream'
            
            print(f"Uploading {local_path} to {s3_path}")
            
            # Upload the file
            with open(local_path, 'rb') as file:
                s3.upload_fileobj(
                    file,
                    bucket,
                    s3_path,
                    ExtraArgs={
                        'ContentType': content_type,
                        'ACL': 'public-read'
                    }
                )

# Define the directories to migrate
directories_to_migrate = {
    'static/glass': 'media/glass',
    'static/doors': 'media/doors',
    'static/colours': 'media/colours'
}

# Perform the migration
for local_dir, r2_prefix in directories_to_migrate.items():
    if os.path.exists(local_dir):
        print(f"\nMigrating {local_dir} to {r2_prefix}")
        upload_directory(local_dir, BUCKET_NAME, r2_prefix)
    else:
        print(f"\nWarning: Directory {local_dir} does not exist") 