from django import template

register = template.Library()

@register.filter
def format_filesize(value):
    if value is None:
        return "N/A"
    return f"{value:.2f} MB"
