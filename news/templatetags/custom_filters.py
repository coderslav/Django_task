from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='censor')
@stringfilter
def censor(value):
    if ("плохое слово 1" or "плохое слово 2" or "плохое слово 3") in value:
        return value.replace("плохое слово 1", "***").replace("плохое слово 2", "***").replace("плохое слово 3", "***")
    else:
        return value
