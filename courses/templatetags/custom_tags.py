from django import template

register = template.Library()

@register.filter
def is_trainer(user):
    return user.groups.filter(name='Trainer').exists()
