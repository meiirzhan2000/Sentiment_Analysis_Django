from django import template

register = template.Library()

@register.filter
def add(value, arg):
    """Add the arg to the value."""
    return float(value) + float(arg)

@register.filter
def multiply(value, arg):
    """Multiply the value by the arg."""
    return float(value) * float(arg)