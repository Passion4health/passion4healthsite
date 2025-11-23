#!/usr/bin/env python
"""
Test script to verify S3 storage configuration and connectivity.

Usage:
    python scripts/test_s3_connection.py

This script tests:
- S3 credentials and connectivity
- Bucket access
- File upload/download
- Storage backend configuration
"""

import os
import sys
import django
from pathlib import Path
from dotenv import load_dotenv

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Load environment variables from .env file
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"Loaded environment variables from {env_path}\n")
else:
    print(f"Warning: .env file not found at {env_path}\n")

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'passion4health.settings.dev')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def test_s3_credentials():
    """Test S3 credentials and basic connectivity."""
    print("=" * 60)
    print("Testing S3 Credentials and Connectivity")
    print("=" * 60)
    
    if not getattr(settings, 'USE_S3_STORAGE', False):
        print("❌ USE_S3_STORAGE is not enabled in settings")
        print("   Set USE_S3_STORAGE=True in your .env file")
        return False
    
    print("✓ USE_S3_STORAGE is enabled")
    
    # Check required settings
    required_settings = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_STORAGE_BUCKET_NAME',
        'AWS_S3_REGION_NAME',
    ]
    
    missing_settings = []
    for setting in required_settings:
        value = getattr(settings, setting, None)
        if not value:
            missing_settings.append(setting)
            print(f"❌ {setting} is not set")
        else:
            # Mask sensitive values
            if 'KEY' in setting or 'SECRET' in setting:
                masked = value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else '****'
                print(f"✓ {setting}: {masked}")
            else:
                print(f"✓ {setting}: {value}")
    
    if missing_settings:
        print(f"\n❌ Missing required settings: {', '.join(missing_settings)}")
        return False
    
    return True


def test_boto3_connection():
    """Test direct boto3 connection to S3."""
    print("\n" + "=" * 60)
    print("Testing Boto3 S3 Connection")
    print("=" * 60)
    
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=getattr(settings, 'AWS_S3_ENDPOINT_URL', None),
        )
        
        # Test bucket access
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        print(f"Testing access to bucket: {bucket_name}")
        
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            print(f"✓ Successfully connected to bucket: {bucket_name}")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                print(f"❌ Bucket '{bucket_name}' does not exist")
            elif error_code == '403':
                print(f"❌ Access denied to bucket '{bucket_name}'")
                print("   Check your AWS credentials and bucket permissions")
            else:
                print(f"❌ Error accessing bucket: {e}")
            return False
            
    except NoCredentialsError:
        print("❌ AWS credentials not found")
        return False
    except Exception as e:
        print(f"❌ Error connecting to S3: {e}")
        return False


def test_django_storage_backend():
    """Test Django storage backend."""
    print("\n" + "=" * 60)
    print("Testing Django Storage Backend")
    print("=" * 60)
    
    try:
        # Check storage backend
        storage_backend = settings.STORAGES['default']['BACKEND']
        print(f"Storage backend: {storage_backend}")
        
        # Test file operations
        test_file_name = 'test_s3_connection.txt'
        test_content = b'This is a test file for S3 storage verification.'
        
        print(f"\nUploading test file: {test_file_name}")
        file_obj = ContentFile(test_content)
        saved_path = default_storage.save(test_file_name, file_obj)
        print(f"✓ File uploaded successfully: {saved_path}")
        
        # Test file exists
        if default_storage.exists(saved_path):
            print(f"✓ File exists check passed: {saved_path}")
        else:
            print(f"❌ File exists check failed: {saved_path}")
            return False
        
        # Test file read
        print(f"Reading file: {saved_path}")
        with default_storage.open(saved_path, 'rb') as f:
            content = f.read()
            if content == test_content:
                print(f"✓ File read successful, content matches")
            else:
                print(f"❌ File content mismatch")
                return False
        
        # Test file URL
        try:
            file_url = default_storage.url(saved_path)
            print(f"✓ File URL generated: {file_url}")
        except Exception as e:
            print(f"⚠ Warning: Could not generate file URL: {e}")
        
        # Clean up - delete test file
        print(f"\nCleaning up test file: {saved_path}")
        default_storage.delete(saved_path)
        if not default_storage.exists(saved_path):
            print(f"✓ Test file deleted successfully")
        else:
            print(f"⚠ Warning: Test file still exists after deletion")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing storage backend: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_static_storage():
    """Test static files storage if configured."""
    print("\n" + "=" * 60)
    print("Testing Static Files Storage")
    print("=" * 60)
    
    try:
        from django.contrib.staticfiles.storage import staticfiles_storage
        
        storage_backend = settings.STORAGES['staticfiles']['BACKEND']
        print(f"Static files storage backend: {storage_backend}")
        
        # Check if staticfiles storage is S3-based
        if 's3' in storage_backend.lower() or 'boto' in storage_backend.lower():
            print("✓ Static files are configured to use S3")
            
            # Test URL generation
            try:
                test_url = staticfiles_storage.url('admin/css/base.css')
                print(f"✓ Static file URL generation works: {test_url}")
            except Exception as e:
                print(f"⚠ Warning: Static file URL generation failed: {e}")
        else:
            print("ℹ Static files are using local storage (not S3)")
        
        return True
        
    except Exception as e:
        print(f"⚠ Warning: Could not test static storage: {e}")
        return True  # Not critical if static storage test fails


def main():
    """Run all S3 tests."""
    print("\n" + "=" * 60)
    print("S3 Storage Configuration Test Suite")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Credentials
    results.append(("Credentials Check", test_s3_credentials()))
    
    if not results[0][1]:
        print("\n❌ Credentials check failed. Please fix configuration before continuing.")
        return False
    
    # Test 2: Boto3 Connection
    results.append(("Boto3 Connection", test_boto3_connection()))
    
    # Test 3: Django Storage Backend
    results.append(("Django Storage Backend", test_django_storage_backend()))
    
    # Test 4: Static Storage
    results.append(("Static Files Storage", test_static_storage()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! S3 storage is configured correctly.")
    else:
        print("\n⚠ Some tests failed. Please review the errors above.")
    
    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

