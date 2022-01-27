from django import template
import datetime

register = template.Library()


@register.filter
def get_datetime(epoch):
    try:
        return datetime.datetime.fromtimestamp(int(epoch)/1000)
    except Exception as e:
        return None
