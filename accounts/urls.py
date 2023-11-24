from django.urls import path

from accounts import views

app_name = 'accounts'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('login/verifyemail', views.verify_email_view, name='verify_email'),
    path('activatetoken/<str:username>/', views.activate_view, name='activate_token'),
    path('createprofile/', views.create_profile_view, name='create_profile'),
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('profile/<str:username>/follow', views.follow_view, name='follow'),
    path('profile/<str:username>/edit', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/changepassword', views.change_password_view, name='change_password'),
    path('', views.test_view, name='test'),
]
