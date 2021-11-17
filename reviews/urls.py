from django.urls import path
from . import views
app_name = 'reviews'
urlpatterns = [
    # adventure_location views
    path('delete/', views.delete, name='delete'),
]
