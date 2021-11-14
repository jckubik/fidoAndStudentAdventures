from django.urls import path
from . import views
app_name = 'adventures'
urlpatterns = [
    # adventure_location views
    path('', views.home, name='home'),
    path('locations', views.adventure_location_list, name='adventure_location_list'),
    path('locations/<int:location_id>', views.adventure_location_detail, name='adventure_location_detail'),
    path('locations/adventure-creator', views.adventure_creator, name='adventure_creator'),
    path('locations/adventure-editor/<int:location_id>', views.edit_location, name='edit_location'),
    path('locations/delete-location/<int:location_id>', views.delete_location, name='delete_location'),
]
