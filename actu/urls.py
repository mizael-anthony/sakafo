from django.urls import path

from . import views

urlpatterns = [
    path(r'^actu/post/(?P<slug>[^\.]+).html', views.view_post, name='view_blog_post'),
    path(r'^actu/category/(?P<slug>[^\.]+).html', views.view_category, name='view_blog_category'),
]