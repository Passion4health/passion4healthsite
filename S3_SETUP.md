# S3 Storage Setup Guide

This guide explains how to configure S3-based storage for your Wagtail project.

## Overview

The project has been configured to support both local file storage and S3-compatible storage (AWS S3, MinIO, etc.). You can switch between them using environment variables.

## Installation

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `boto3` - AWS SDK for Python
   - `django-storages` - Django storage backends for cloud storage

## Configuration

### 1. Environment Variables

Copy `example.env` to `.env` and configure the following variables:

```bash
# Enable S3 storage
USE_S3_STORAGE=True

# AWS S3 Credentials (Required)
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Optional: For MinIO or S3-compatible storage
AWS_S3_ENDPOINT_URL=https://your-minio-endpoint.com
AWS_S3_ADDRESSING_STYLE=path

# Optional: Custom domain (e.g., CloudFront)
AWS_S3_CUSTOM_DOMAIN=cdn.yourdomain.com

# Optional: Storage options
AWS_DEFAULT_ACL=public-read
AWS_S3_FILE_OVERWRITE=False
AWS_QUERYSTRING_AUTH=False
AWS_LOCATION=  # Optional prefix/path within bucket
```

### 2. AWS S3 Setup

For AWS S3:

1. Create an S3 bucket in your AWS account
2. Create an IAM user with S3 access permissions
3. Generate access keys for the IAM user
4. Set the bucket name and region in `.env`

**Required IAM Permissions:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```

### 3. MinIO Setup

For MinIO (self-hosted S3-compatible storage):

1. Set up MinIO server
2. Create a bucket
3. Create access keys
4. Set `AWS_S3_ENDPOINT_URL` to your MinIO endpoint
5. Optionally set `AWS_S3_ADDRESSING_STYLE=path` if needed

## Project Structure

### Storage Configuration

- **`passion4health/settings/base.py`** - Main settings file with S3 configuration
- **`passion4health/storage.py`** - Custom storage backends for static and media files

### Storage Backends

The project uses custom storage classes:

- **`MediaStorage`** - Handles media files (images, documents, etc.)
  - Location: `media/` (or `{AWS_LOCATION}/media/` if set)
  
- **`StaticStorage`** - Handles static files (CSS, JS, etc.)
  - Location: `static/` (or `{AWS_LOCATION}/static/` if set)

## Testing

Run the test scripts to verify your S3 configuration:

```bash
# Test S3 connection and configuration
python scripts/test_s3_connection.py

# Test file operations
python scripts/test_s3_file_operations.py

# Test Wagtail integration
python scripts/test_wagtail_s3_integration.py
```

See `scripts/README.md` for detailed information about each test script.

## Usage

### Switching Between Local and S3 Storage

**Local Storage (Default):**
```bash
USE_S3_STORAGE=False
```

**S3 Storage:**
```bash
USE_S3_STORAGE=True
# ... configure AWS credentials
```

### Collecting Static Files to S3

When using S3 for static files, run:

```bash
python manage.py collectstatic --noinput
```

This will upload all static files to your S3 bucket.

### Wagtail Media Files

Wagtail will automatically use S3 storage for:
- Image uploads (via Wagtail admin)
- Document uploads (via Wagtail admin)
- Any file fields in your models

## File Organization in S3

When using S3 storage, files are organized as follows:

```
your-bucket/
├── static/          # Static files (CSS, JS, etc.)
│   ├── admin/
│   ├── css/
│   └── ...
└── media/          # Media files (images, documents, etc.)
    ├── images/     # Wagtail images
    ├── documents/  # Wagtail documents
    └── ...
```

If `AWS_LOCATION` is set (e.g., `production/`), the structure becomes:

```
your-bucket/
└── production/
    ├── static/
    └── media/
```

## URL Configuration

When using S3 storage:
- Media files are served directly from S3 (via S3 URLs or custom domain)
- Static files are served from S3 (via S3 URLs or custom domain)
- The local media/static URL patterns in `urls.py` are not used

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'storages'"**
   - Run: `pip install -r requirements.txt`

2. **"Access Denied" errors**
   - Check IAM permissions for your AWS credentials
   - Verify bucket name is correct
   - Ensure bucket exists and is accessible

3. **Files not appearing in S3**
   - Check bucket permissions
   - Verify `AWS_STORAGE_BUCKET_NAME` is correct
   - Check `AWS_LOCATION` prefix if set

4. **URLs not working**
   - Verify `AWS_S3_CUSTOM_DOMAIN` if using a CDN
   - Check bucket CORS settings if accessing from browser
   - Ensure `AWS_DEFAULT_ACL` allows public read if needed

### Debugging

Enable debug logging in `settings/base.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'storages': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'boto3': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Security Considerations

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Use IAM roles** in production (AWS) instead of access keys when possible
3. **Set appropriate ACLs** - Use `private` for sensitive files, `public-read` for public assets
4. **Use signed URLs** - Set `AWS_QUERYSTRING_AUTH=True` for private file access
5. **Enable CORS** on your S3 bucket if serving files to web browsers
6. **Use CloudFront** or similar CDN for better performance and security

## Production Checklist

- [ ] S3 bucket created and configured
- [ ] IAM user/role with appropriate permissions
- [ ] Environment variables set in production environment
- [ ] `USE_S3_STORAGE=True` in production
- [ ] Static files collected to S3 (`collectstatic`)
- [ ] CORS configured on S3 bucket (if needed)
- [ ] Custom domain/CDN configured (optional but recommended)
- [ ] Test scripts pass successfully
- [ ] Backup strategy for S3 data

## Additional Resources

- [django-storages documentation](https://django-storages.readthedocs.io/)
- [boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Wagtail deployment guide](https://docs.wagtail.org/en/stable/advanced_topics/deploying.html)
- [AWS S3 documentation](https://docs.aws.amazon.com/s3/)

