from django.urls import path
from .views import PostList,PostDetail
from . import views
app_name = 'blog'
urlpatterns = [
 # post views
 path('', PostList.as_view(), name='post_list'),
  path('', views.post_list, name='post_list'),
 path('tag/<slug:tag_slug>/',
 views.post_list, name='post_list_by_tag'),
 path('<str:slug>/<int:day>/<int:month>/<int:year>', views.post_detail, name='post_detail'),
 path('<int:post_id>/share/',
 views.post_share, name='post_share'),
path('<int:post_id>/comment/',
 views.post_comment, name='post_comment'),
path('post_publish',
 views.post_publish, name='post_publish'),
]