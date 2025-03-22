from django import template

register = template.Library()

@register.filter(name='filter_section')
def filter_section(sections, section_type):
    """Returns the section of given type"""
    try:
        return sections.filter(section_type=section_type).first()
    except AttributeError:
        return None

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplies the value by the argument"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''