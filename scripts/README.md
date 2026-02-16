# S3 Storage Test Scripts

This directory contains test scripts for verifying S3 storage configuration and functionality in the Wagtail project.

## Prerequisites

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Configure your `.env` file with S3 credentials (see `example.env` for reference)

3. Set `USE_S3_STORAGE=True` in your `.env` file to enable S3 storage

## Test Scripts

### 1. `test_s3_connection.py`

Tests S3 connectivity and basic configuration.

**What it tests:**

- S3 credentials validation
- Boto3 connection to S3
- Bucket access permissions
- Django storage backend configuration
- Static files storage configuration

**Usage:**

```bash
python scripts/test_s3_connection.py
```

**Expected output:**

- ✓ Credentials check
- ✓ Boto3 connection
- ✓ Django storage backend
- ✓ Static files storage

### 2. `test_s3_file_operations.py`

Tests file operations on S3 storage.

**What it tests:**

- Text file upload/download
- Binary file upload/download
- Large file upload (1MB+)
- File overwrite behavior
- File URL generation
- File listing (if supported)

**Usage:**

```bash
python scripts/test_s3_file_operations.py
```

**Expected output:**

- ✓ Text file upload
- ✓ Binary file upload
- ✓ Large file upload
- ✓ File overwrite
- ✓ File URL generation
- ✓ File listing

### 3. `test_wagtail_s3_integration.py`

Tests Wagtail-specific S3 integration.

**What it tests:**

- Wagtail image uploads to S3
- Wagtail document uploads to S3
- Image serving from S3
- Document serving from S3
- Storage backend configuration for Wagtail

**Usage:**

```bash
python scripts/test_wagtail_s3_integration.py
```

**Expected output:**

- ✓ Storage backend configuration
- ✓ Wagtail image storage
- ✓ Wagtail document storage

## Running All Tests

To run all test scripts:

```bash
# Test connection
python scripts/test_s3_connection.py

# Test file operations
python scripts/test_s3_file_operations.py

# Test Wagtail integration
python scripts/test_wagtail_s3_integration.py
```

## Troubleshooting

### Common Issues

1. **"USE_S3_STORAGE is not enabled"**

   - Set `USE_S3_STORAGE=True` in your `.env` file

2. **"AWS credentials not found"**

   - Ensure `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are set in `.env`

3. **"Bucket does not exist"**

   - Create the bucket in your S3/MinIO instance
   - Ensure the bucket name matches `AWS_STORAGE_BUCKET_NAME` in `.env`

4. **"Access denied to bucket"**

   - Check IAM permissions for your AWS credentials
   - For MinIO, ensure the access key has proper permissions

5. **Import errors**
   - Run `pip install -r requirements.txt` to install all dependencies
   - Ensure `django-storages` and `boto3` are installed

## Environment Variables

Required environment variables (set in `.env`):

```bash
USE_S3_STORAGE=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

Optional environment variables:

```bash
AWS_S3_ENDPOINT_URL=https://your-minio-endpoint.com  # For MinIO
AWS_S3_CUSTOM_DOMAIN=cdn.yourdomain.com              # For CloudFront/CDN
AWS_DEFAULT_ACL=public-read                           # File permissions
AWS_S3_FILE_OVERWRITE=False                          # Overwrite existing files
AWS_QUERYSTRING_AUTH=False                           # Signed URLs
AWS_LOCATION=                                         # Bucket prefix/path
```

## Notes

- Test scripts create temporary files in S3 for testing and clean them up automatically
- All test files are prefixed with `test_files/` or `test_` for easy identification
- Scripts use the `dev` settings by default - modify the `DJANGO_SETTINGS_MODULE` in scripts if needed
- For production testing, ensure you're using a test bucket, not production data
