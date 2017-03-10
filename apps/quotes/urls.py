from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^quotes$', views.quotes, name='quotes'),
    url(r'^post_quote$', views.post_quote, name='post_quote'),
    url(r'^users/(?P<id>\d+)$', views.user, name='user'),
    url(r'^add_to_list/(?P<id>\d+)$', views.add_to_list, name='add_to_list'),
    url(r'^remove/(?P<id>\d+)$', views.remove, name='remove')
]
