from django.conf.urls import patterns, url

from logout import views

urlpatterns = patterns('',
    url(r'^$', views.logout, name='logout')
)

