"""AskThem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myapp import views as ask_views
from django.conf.urls.static import static
import django.contrib.auth.views
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup$', ask_views.signup, name='signup'),
    url(r'^login$', ask_views.login_page, name='login_page'),
    url(r'^ask$', ask_views.ask, name='ask'),
    url(r'^hot$', ask_views.hot_questions, name='hot_questions'),
    url(r'^tag/(?P<tag>\w*)$', ask_views.tags_question, name='tag_questions'),
    url(r'^question/(?P<q_id>\d+)$', ask_views.id_question, name='id_question'),
    url(r'^$', ask_views.new_questions, name='new_questions'),
    url(r'^logout$', ask_views.logout_page, name='logout_page'),
    url(r'^profile/(?P<username>\w*)$', ask_views.profile, name='profile'),
    url(r'^changeinfo$', ask_views.change_info, name='change_info'),
    url(r'^changepassword$', ask_views.change_password, name='change_password'),
    url(r'^changepic$', ask_views.change_pic, name='change_pic'),
    url(r'^correct$', ask_views.correct, name='correct'),
    url(r'^like$', ask_views.like, name='like'),
    url(r'^single_answer$', ask_views.single_answer, name='single_answer'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
