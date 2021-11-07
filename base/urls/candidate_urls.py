from django.urls import path
from base.views import candidate_views as views

urlpatterns = [
    path('list_candidates/', views.getCandidates, name='list_candidates'),
    path('candidate_details/', views.getCandidateDetails, name='candidate_details'),
    path('create_candidate/', views.createCandidate, name='create_candidate'),
    path('delete_candidate/', views.deleteCandidate, name='delete_candidate'),
    path('update_candidate/', views.updateCandidate, name='update_candidate'),
]
