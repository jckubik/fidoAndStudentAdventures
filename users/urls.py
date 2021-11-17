from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    # adventure_location views
    path('register/', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('list/', views.user_list, name='list'),
    path('edit/<str:username>', views.edit_user, name='edit'),
]
