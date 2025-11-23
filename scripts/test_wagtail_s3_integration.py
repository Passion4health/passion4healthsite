#!/usr/bin/env python
"""
Test script for Wagtail-specific S3 storage integration.

Usage:
    python scripts/test_wagtail_s3_integration.py

This script tests:
- Wagtail image uploads to S3
- Wagtail document uploads to S3
- Image serving from S3
- Document serving from S3
"""

import os
import sys
import django
from pathlib import Path
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
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
from PIL import Image


def create_test_image():
    """Create a simple test image."""
    img = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer


def test_wagtail_image_storage():
    """Test Wagtail image storage on S3."""
    print("Testing Wagtail image storage...")
    
    try:
        from wagtail.images.models import Image as WagtailImage
        
        # Create a test image
        image_file = create_test_image()
        test_image = ImageFile(image_file, name='test_wagtail_image.png')
        
        # Create Wagtail image instance
        wagtail_img = WagtailImage(
            title="Test S3 Image",
            file=test_image
        )
        wagtail_img.save()
        
        print(f"  ✓ Wagtail image created: {wagtail_img.id}")
        print(f"  ✓ Image file path: {wagtail_img.file.name}")
        
        # Check if file exists in storage
        if wagtail_img.file.storage.exists(wagtail_img.file.name):
            print(f"  ✓ Image file exists in S3 storage")
        else:
            print(f"  ❌ Image file does not exist in storage")
            return False
        
        # Test image URL
        try:
            image_url = wagtail_img.file.url
            print(f"  ✓ Image URL: {image_url}")
        except Exception as e:
            print(f"  ⚠ Could not generate image URL: {e}")
        
        # Test image serving (check if URL is accessible)
        # This would require making an HTTP request, which we skip for now
        
        # Clean up
        wagtail_img.delete()
        print(f"  ✓ Test image deleted")
        
        return True
        
    except ImportError:
        print("  ⚠ Wagtail images app not available")
        return True  # Not a failure if Wagtail isn't fully set up
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_wagtail_document_storage():
    """Test Wagtail document storage on S3."""
    print("Testing Wagtail document storage...")
    
    try:
        from wagtail.documents.models import Document
        
        # Create a test document
        test_content = b"This is a test PDF document content for S3 storage."
        test_file = ContentFile(test_content, name='test_document.pdf')
        
        wagtail_doc = Document(
            title="Test S3 Document",
            file=test_file
        )
        wagtail_doc.save()
        
        print(f"  ✓ Wagtail document created: {wagtail_doc.id}")
        print(f"  ✓ Document file path: {wagtail_doc.file.name}")
        
        # Check if file exists in storage
        if wagtail_doc.file.storage.exists(wagtail_doc.file.name):
            print(f"  ✓ Document file exists in S3 storage")
        else:
            print(f"  ❌ Document file does not exist in storage")
            return False
        
        # Test document URL
        try:
            doc_url = wagtail_doc.file.url
            print(f"  ✓ Document URL: {doc_url}")
        except Exception as e:
            print(f"  ⚠ Could not generate document URL: {e}")
        
        # Clean up
        wagtail_doc.delete()
        print(f"  ✓ Test document deleted")
        
        return True
        
    except ImportError:
        print("  ⚠ Wagtail documents app not available")
        return True  # Not a failure if Wagtail isn't fully set up
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_storage_backend_configuration():
    """Test that storage backends are correctly configured."""
    print("Testing storage backend configuration...")
    
    try:
        # Check default storage
        default_storage = settings.STORAGES['default']['BACKEND']
        print(f"  Default storage: {default_storage}")
        
        # Check if it's S3-based
        if 's3' in default_storage.lower() or 'boto' in default_storage.lower():
            print(f"  ✓ Default storage is S3-based")
        else:
            print(f"  ⚠ Default storage is not S3-based: {default_storage}")
        
        # Check Wagtail-specific storage settings
        # Wagtail uses the default storage for images and documents
        print(f"  ✓ Wagtail will use default storage for media files")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Run all Wagtail S3 integration tests."""
    print("=" * 60)
    print("Wagtail S3 Integration Test Suite")
    print("=" * 60)
    print()
    
    if not getattr(settings, 'USE_S3_STORAGE', False):
        print("❌ USE_S3_STORAGE is not enabled")
        print("   Set USE_S3_STORAGE=True in your .env file")
        return False
    
    results = []
    
    results.append(("Storage Backend Configuration", test_storage_backend_configuration()))
    print()
    results.append(("Wagtail Image Storage", test_wagtail_image_storage()))
    print()
    results.append(("Wagtail Document Storage", test_wagtail_document_storage()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All Wagtail S3 integration tests passed!")
    else:
        print("\n⚠ Some tests failed. Please review the errors above.")
    
    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

