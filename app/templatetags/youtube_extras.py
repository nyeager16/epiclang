from django import template
import re

register = template.Library()

@register.filter
def youtube_id(url):
    """
    Extract the YouTube video ID from the URL.
    """
    regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(regex, url)
    return match.group(1) if match else url