from django.conf.urls import patterns, url

from buy import views

urlpatterns = patterns('',
    url(r'^$', views.buy, name='buy')
)

