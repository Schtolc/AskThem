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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup', ask_views.signup, name='signup'),
    url(r'^login', ask_views.login, name='login'),
    url(r'^ask', ask_views.ask, name='ask'),
    url(r'^hot', ask_views.hot_questions, name='hot_questions'),
    url(r'^tag/(?P<tag>\w+)', ask_views.tags_question, name='tag_questions'),
    url(r'^question/(?P<q_id>\d+)', ask_views.id_question, name='id_question'),
    url(r'^', ask_views.new_questions, name='new_questions'),
]
