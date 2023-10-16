from django.urls import path
from csv_parser.files.views import (
    upload_csv,
    FilesIndexView,
    FileDetailView,
    FileDeleteView,
    show_data,
    download_file
)


urlpatterns = [
    path('upload/', upload_csv, name="upload"),
    path('list/', FilesIndexView.as_view(), name="index"),
    path('<int:pk>/', FileDetailView.as_view(), name="file_details"),
    path('<int:pk>/data', show_data, name='show_frame'),
    path('<int:pk>/download', download_file, name='download_file'),
    path('<int:pk>/delete', FileDeleteView.as_view(), name='delete_file'),
]
