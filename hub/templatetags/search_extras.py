from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
import re

register = template.Library()


@register.filter
def highlight_search(text, query):
   
    if not text or not query:
        return text
    
    
    escaped_text = escape(text)
    
    
    terms = [term.strip() for term in query.split() if term.strip()]
    
    if not terms:
        return escaped_text
    
    
    pattern_parts = []
    for term in terms:
        escaped_term = re.escape(term)
        pattern_parts.append(escaped_term)
    
    pattern = '|'.join(pattern_parts)
    regex = re.compile(f'({pattern})', re.IGNORECASE)
    
    def replace_func(match):
        return f'<mark class="bg-cyan-500/30 text-cyan-200 rounded px-1">{match.group(1)}</mark>'
    
    highlighted = regex.sub(replace_func, escaped_text)
    return mark_safe(highlighted)