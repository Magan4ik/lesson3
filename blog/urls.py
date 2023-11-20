from django.urls import path

from blog import views

app_name = 'blog'


urlpatterns = [
    path('detail/post/<str:slug_name>/', views.post_detail_view, name='detail'),
    path('detail/comment/<int:comment_id>/like/', views.add_commentlike_view, name='add_commentlike'),
    path('detail/comment/<int:comment_id>/dislike/', views.add_commentdislike_view, name='add_commentdislike'),
    path('detail/post/<str:slug_name>/like/', views.add_postlike_view, name='add_postlike'),
    path('detail/post/<str:slug_name>/dislike/', views.add_postdislike_view, name='add_postdislike'),
    path('', views.post_list_view, name='post_list'),
]
