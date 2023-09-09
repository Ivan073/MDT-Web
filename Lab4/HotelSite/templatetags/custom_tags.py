import datetime
import random

from django import template
import pytz

register = template.Library()

@register.simple_tag(takes_context=True)
def current_time(context, format_string):
    user_tz = user_timezone(context)
    utc_now = datetime.datetime.utcnow()
    if user_tz == 'Not determined':
        user_tz = pytz.timezone('Europe/Minsk')
    user_now = utc_now.replace(tzinfo=pytz.utc).astimezone(user_tz)
    return user_now.strftime(format_string)

@register.simple_tag(takes_context=True)
def user_timezone(context):
    request = context['request']
    tzname = request.COOKIES.get('django_timezone')
    if tzname:
        return pytz.timezone(tzname)
    else:
        return 'Not determined'

@register.simple_tag(takes_context=True)
def random_tag(context):
    return random.randint(1,100)