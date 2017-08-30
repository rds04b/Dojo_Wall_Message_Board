from django.conf.urls import url
from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^create_message$', views.create_message, name='create_message'),
    url(r'^create_comment/(?P<id>\d+)$', views.create_comment, name='create_comment'),
    url(r'^like/(?P<id>\d+)$', views.like, name="like"),
    url(r'^like_comment/(?P<id>\d+)$', views.like_comment, name="like_comment"),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^delete_comment/(?P<id>\d+)$', views.delete_comment, name='delete_comment'),
    url(r'^most$', views.most, name='most'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^results$', views.results, name='results')
]
