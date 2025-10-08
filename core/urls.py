from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('shorts/', views.shorts_view, name='shorts'),
    path('videos/', views.all_videos_view, name='all_videos'),  # Dedicated other videos page
    path("plants/", views.plants_list, name="plants_list"),
    path("plants/autocomplete/", views.plant_autocomplete, name="plant_autocomplete"),
    
]
