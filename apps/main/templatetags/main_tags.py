from django.template.defaulttags import register

@register.filter
def attr(object, key):
    if hasattr(object, key):
        return getattr(object, key)
    return object.get(key)

@register.filter
def title(s):
    return s.replace('_', ' ').title()