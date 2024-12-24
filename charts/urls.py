from django.urls import path
from . import views

app_name = 'charts'
urlpatterns = [
    path('', views.index, name="index"),
    path('generate', views.generate, name='generate'),
    path('charts', views.chart_display, name='chart_display'),
]