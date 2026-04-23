import os
from django import template
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def inline_svg(file_field):
    if not file_field or not str(file_field.url).lower().rstrip().endswith(".svg"):
        return "Not an SVG file"
    try:
        # Wagtail renditions (and other FileField-backed objects) use default_storage.
        # This works for local files and S3/MinIO; the old MEDIA_ROOT path does not
        # exist in Docker when media lives only in object storage.
        field_file = getattr(file_field, "file", None)
        if field_file and getattr(field_file, "name", None):
            with field_file.open("rb") as f:
                return mark_safe(f.read().decode("utf-8"))

        # Fallback: path under MEDIA_ROOT (local / dev)
        relative_path = str(file_field.url).replace(str(settings.MEDIA_URL), "", 1).lstrip(
            "/"
        )
        file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as svg_file:
                return mark_safe(svg_file.read())

        if relative_path and default_storage.exists(relative_path):
            with default_storage.open(relative_path) as f:
                return mark_safe(f.read().decode("utf-8"))

        return "File not found"
    except Exception as e:
        return f"Error: {str(e)}"
