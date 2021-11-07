from django.urls import path
from base.views import selection_process_views as views

urlpatterns = [
    path('list_selection_process/', views.getSelectionProcess, name='list_selection_process'),
    path('selection_process_details/', views.getSelectionProcessDetails, name='selection_process_details'),
    path('create_selection_process/', views.createSelectionProcess, name='create_selection_process'),
    path('delete_selection_process/', views.deleteSelectionProcess, name='delete_selection_process'),
    path('update_selection_process/', views.updateSelectionProcess, name='update_selection_process'),
    path('selection_process_insert_candidate/', views.insertCandidate, name='selection_process_insert_candidate'),
    path('selection_process_remove_candidate/', views.removeCandidate, name='selection_process_remove_candidate'),
    path('approved_candidates/', views.getSelectionProcessResult, name='approved_candidates'),
]

