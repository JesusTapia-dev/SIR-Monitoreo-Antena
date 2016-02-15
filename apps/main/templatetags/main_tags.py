from django.template.defaulttags import register

@register.filter
def attr(instance, key):
    
    display_key = "get_" + key + "_display"
    
    if hasattr(instance, display_key):
        return getattr(instance, display_key)()
    
    if hasattr(instance, key):
        return getattr(instance, key)
    
    return instance.get(key)

@register.filter
def title(s):
    return s.replace('_', ' ').title()

@register.filter
def value(instance, key):
    
    item = instance
    for my_key in key.split("__"):
        print "TP Value", item, my_key
        item = attr(item, my_key)
    
    print item
    return item

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()