from django.urls import path
from . import views

app_name = 'statistic'
urlpatterns = [
     path('', views.StatisticsView.as_view(), name='statistics'),
]
