from django.urls import path
from base.views import team_views as views

urlpatterns = [
    path('list_teams/', views.getTeams, name='list_teams'),
    path('team_details/', views.getTeamDetails, name='team_details'),
    path('create_team/', views.createTeam, name='create_team'),
    path('delete_team/', views.deleteTeam, name='delete_team'),
    path('update_team/', views.updateTeam, name='update_team'),
]
