from django import template

register = template.Library()

@register.filter
def full_url(page, request):
    return f"{request.site.root_url}{page.url}"
