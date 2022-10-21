from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('event/<int:event_id>/match/<int:match_number>/', views.match_details, name="match results"),
    path('team/<int:team_number>/', views.team_details, name="aggregated team results"),
    path('event/<int:event_id>/team/<int:team_number>/', views.team_at_event),
    path('event/<int:event_id>/team/<int:team_number>/match/<int:match_number>/', views.team_on_match, name="team results on specific match"),
    path('event/<int:event_id>/match/<int:match_number>/team/<int:team_number>/', views.team_on_match, name="match results for specific team number"),
    path('event/<int:event_id>/', views.event_details),
    path('scan/', views.scan_code)
]

