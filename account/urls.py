from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
    url(r'^create_account/', views.create_account, name='create_account'),
    url(r'^top_up_account/', views.top_up_account, name='top_up_account'),
    url(r'^view_account/', views.view_account, name='view_account'),
    url(r'^change_pin/', views.change_pin, name='change_pin'),

)
