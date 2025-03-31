from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'), 
    path('register1org/', views.registerorg_view, name='register1org'), # Update the view function name
    path('players/', views.display_players, name='display_players'),
]


