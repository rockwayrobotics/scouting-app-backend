from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "event/<int:event_id>/match/<int:this_match_number>/",
        views.match_details,
        name="match results",
    ),
    path("team/<int:team_number>/", views.team_details, name="aggregated team results"),
    path("event/<int:event_id>/team/<int:team_number>/", views.team_at_event),
    path(
        "event/<int:event_id>/team/<int:team_number>/match/<int:this_match_number>/",
        views.team_on_match,
        name="team results on specific match",
    ),
    path(
        "event/<int:event_id>/match/<int:this_match_number>/team/<int:team_number>/",
        views.team_on_match,
        name="match results for specific team number",
    ),
    path("event/<int:event_id>/", views.event_details),
    path("event/", views.event_list),
    path("team/", views.team_list),
    path("scan/", views.scan, name='scan-qr'),
    path("vis/", views.vis_test),

    path("entry_page/", views.entry_page, name='entry-page'),
    path("events_schedule/", views.events_schedule, name='events-schedule'),
    path("matches_schedule/", views.matches_schedule, name='matches-schedule'),
    path("team_stats/", views.team_stats, name='team-stats'),
    path("match_stats/", views.match_stats, name='match-stats'),
]
