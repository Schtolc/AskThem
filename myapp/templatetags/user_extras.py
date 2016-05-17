from django import template
from django.contrib.auth.models import User
from myapp.models import *
from django.core.cache import cache

register = template.Library()


@register.simple_tag()
def is_disabled(q_id, u_id, is_like):
    if not u_id:
        return 'disabled'
    l = Like.objects.filter(question=Question.objects.get(id=q_id)).filter(user=User.objects.get(id=u_id)).filter(
        is_like=is_like)
    if len(l) != 0:
        return 'disabled'
    else:
        return ''


@register.simple_tag()
def user_pic(u_id):
    u = User.objects.get(id=u_id)
    p = Profile.objects.get(avatar=u)
    return str(p.picture.url)


@register.inclusion_tag("best_users.html")
def best_users():
    data = cache.get('best_users', 'has_expired')
    return {
        'data': data,
    }


@register.inclusion_tag("best_tags.html")
def best_tags():
    data = cache.get('best_tags', 'has_expired')
    return {
        'data': data,
    }