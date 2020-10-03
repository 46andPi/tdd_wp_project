from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'lists/the_only_list_in_the_world/$', views.view_list,
        name='view_list')
]
