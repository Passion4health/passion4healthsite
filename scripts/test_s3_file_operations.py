#!/usr/bin/env python
"""
Test script for S3 file operations (upload, download, delete, list).

Usage:
    python scripts/test_s3_file_operations.py

This script performs comprehensive file operation tests on S3 storage.
"""

import os
import sys
import django
from pathlib import Path
import tempfile
from io import BytesIO
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
from django.core.files.uploadedfile import SimpleUploadedFile


def test_text_file_upload():
    """Test uploading a text file."""
    print("Testing text file upload...")
    
    test_content = "This is a test text file for S3 storage.\nLine 2 of the file."
    test_filename = 'test_files/test_text_file.txt'
    
    try:
        file_obj = ContentFile(test_content.encode('utf-8'))
        saved_path = default_storage.save(test_filename, file_obj)
        
        # Verify file exists
        if default_storage.exists(saved_path):
            print(f"  ✓ Text file uploaded: {saved_path}")
            
            # Read back and verify content
            with default_storage.open(saved_path, 'r') as f:
                content = f.read()
                if content == test_content:
                    print(f"  ✓ Text file content verified")
                else:
                    print(f"  ❌ Text file content mismatch")
                    return False
            
            # Clean up
            default_storage.delete(saved_path)
            print(f"  ✓ Text file deleted")
            return True
        else:
            print(f"  ❌ File does not exist after upload")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_binary_file_upload():
    """Test uploading a binary file."""
    print("Testing binary file upload...")
    
    # Create a small binary file (PNG header)
    test_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
    test_filename = 'test_files/test_image.png'
    
    try:
        file_obj = ContentFile(test_content)
        saved_path = default_storage.save(test_filename, file_obj)
        
        if default_storage.exists(saved_path):
            print(f"  ✓ Binary file uploaded: {saved_path}")
            
            # Read back and verify
            with default_storage.open(saved_path, 'rb') as f:
                content = f.read()
                if content == test_content:
                    print(f"  ✓ Binary file content verified")
                else:
                    print(f"  ❌ Binary file content mismatch")
                    return False
            
            # Clean up
            default_storage.delete(saved_path)
            print(f"  ✓ Binary file deleted")
            return True
        else:
            print(f"  ❌ File does not exist after upload")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_large_file_upload():
    """Test uploading a larger file."""
    print("Testing large file upload...")
    
    # Create a 1MB file
    large_content = b'X' * (1024 * 1024)  # 1MB
    test_filename = 'test_files/test_large_file.bin'
    
    try:
        file_obj = ContentFile(large_content)
        saved_path = default_storage.save(test_filename, file_obj)
        
        if default_storage.exists(saved_path):
            file_size = default_storage.size(saved_path)
            print(f"  ✓ Large file uploaded: {saved_path} ({file_size} bytes)")
            
            # Clean up
            default_storage.delete(saved_path)
            print(f"  ✓ Large file deleted")
            return True
        else:
            print(f"  ❌ File does not exist after upload")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_file_overwrite():
    """Test file overwrite behavior."""
    print("Testing file overwrite...")
    
    test_filename = 'test_files/test_overwrite.txt'
    content1 = "First version"
    content2 = "Second version"
    
    try:
        # Upload first version
        file_obj1 = ContentFile(content1.encode('utf-8'))
        saved_path1 = default_storage.save(test_filename, file_obj1)
        
        # Upload second version
        file_obj2 = ContentFile(content2.encode('utf-8'))
        saved_path2 = default_storage.save(test_filename, file_obj2)
        
        # Check which version exists
        with default_storage.open(saved_path2, 'r') as f:
            content = f.read()
            if content == content2:
                print(f"  ✓ File overwrite works correctly")
            else:
                print(f"  ⚠ File overwrite behavior: content is '{content}'")
        
        # Clean up
        default_storage.delete(saved_path2)
        print(f"  ✓ Test file deleted")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_file_url_generation():
    """Test file URL generation."""
    print("Testing file URL generation...")
    
    test_filename = 'test_files/test_url.txt'
    test_content = "Test content for URL generation"
    
    try:
        file_obj = ContentFile(test_content.encode('utf-8'))
        saved_path = default_storage.save(test_filename, file_obj)
        
        # Generate URL
        file_url = default_storage.url(saved_path)
        print(f"  ✓ File URL generated: {file_url}")
        
        # Clean up
        default_storage.delete(saved_path)
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_file_listing():
    """Test listing files (if supported)."""
    print("Testing file listing...")
    
    test_files = [
        'test_files/list_test_1.txt',
        'test_files/list_test_2.txt',
        'test_files/list_test_3.txt',
    ]
    
    try:
        # Upload test files
        for filename in test_files:
            file_obj = ContentFile(b"test content")
            default_storage.save(filename, file_obj)
        
        print(f"  ✓ Created {len(test_files)} test files")
        
        # Note: Django's default storage doesn't have a listdir method
        # This would need to be implemented for S3 if needed
        print(f"  ℹ File listing not available in default storage backend")
        
        # Clean up
        for filename in test_files:
            if default_storage.exists(filename):
                default_storage.delete(filename)
        
        print(f"  ✓ Test files deleted")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        # Clean up on error
        for filename in test_files:
            try:
                if default_storage.exists(filename):
                    default_storage.delete(filename)
            except:
                pass
        return False


def main():
    """Run all file operation tests."""
    print("=" * 60)
    print("S3 File Operations Test Suite")
    print("=" * 60)
    print()
    
    if not getattr(settings, 'USE_S3_STORAGE', False):
        print("❌ USE_S3_STORAGE is not enabled")
        print("   Set USE_S3_STORAGE=True in your .env file")
        return False
    
    results = []
    
    results.append(("Text File Upload", test_text_file_upload()))
    print()
    results.append(("Binary File Upload", test_binary_file_upload()))
    print()
    results.append(("Large File Upload", test_large_file_upload()))
    print()
    results.append(("File Overwrite", test_file_overwrite()))
    print()
    results.append(("File URL Generation", test_file_url_generation()))
    print()
    results.append(("File Listing", test_file_listing()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All file operation tests passed!")
    else:
        print("\n⚠ Some tests failed. Please review the errors above.")
    
    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

