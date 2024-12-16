from django.urls import path
from .views import create_robot, download_robot_summary, download_summary_page

urlpatterns = [
    path('create-robot/', create_robot, name='create_robot'),
    path('download-robot-summary/', download_robot_summary, name='download_robot_summary'),
    path('download-summary-page/', download_summary_page, name='download_summary_page'),
]
