from django import template
from django.template.defaultfilters import stringfilter
import datetime

register = template.Library()


@register.filter(name='censor')
@stringfilter
def censor(value):
    forbidden_words = ["плохое слово 1", "плохое слово 2", "плохое слово 3"]
    f_words = [word for word in forbidden_words if word in value]
    if f_words:
        new_value = value
        for f_word in f_words:
            new_value = new_value.replace(f_word, f_word[0] + '*' * (len(f_word)-2) + f_word[-1])
        return new_value
    else:
        return value


@register.simple_tag(name='time')
def time(time_format):
    return datetime.datetime.now().strftime(time_format)
