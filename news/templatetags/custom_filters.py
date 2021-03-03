from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    if "плохое слово 1" or "плохое слово 2" or "плохое слово 3" in value:
        value.replace("плохое слово 1", "***")
        value.replace("плохое слово 2", "***")
        value.replace("плохое слово 3", "***")
        return value
    else:
        return value
