"""
Template tags for trainee views.
"""
from datetime import date
from django import template

register = template.Library()


@register.simple_tag
def is_deadline_passed(event):
    """Check if the registration deadline has passed for an event."""
    return date.today() > event.registration_deadline


@register.filter
def is_in_list(value, list_values):
    """Check if a value is in a list."""
    return value in list_values


@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
