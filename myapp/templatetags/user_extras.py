from django import template
from django.contrib.auth.models import User
from myapp.models import Profile

register = template.Library()


@register.simple_tag()
def user_pic(u_id):
    u = User.objects.get(id = u_id)
    p = Profile.objects.get(avatar=u)
    return str(p.picture.url)
