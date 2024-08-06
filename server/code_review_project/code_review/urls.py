# urls.py
from django.urls import re_path, path
from .views import RepoView, AnalysisDetailView, FileContentView, FileAnalysisView

urlpatterns = [
    path('repo/', RepoView.as_view(), name='repo-view'),
    path('analysis/<str:repo_name>/', AnalysisDetailView.as_view(), name='analysis-detail-view'),
    re_path(r'^file/(?P<repo_name>[\w-]+)/(?P<file_path>.+)$', FileContentView.as_view(), name='file-content-view'),
    path('analyze-file/', FileAnalysisView.as_view(), name='analyze-file-view'),
]
