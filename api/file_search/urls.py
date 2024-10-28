from django.urls import path

from search.views import schema_view, CreateSearchView, GetSearchResultsView

urlpatterns = [
    path('docs', schema_view.with_ui(), name='swagger-ui'),
    path('searches', CreateSearchView.as_view(), name='create_search'),
    path('searches/<uuid:search_id>', GetSearchResultsView.as_view(), name='get_search_results'),
]
