from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('health/', views.health_view, name='health'),
    path('delay/', views.delay_view, name='delay'),
    path('error/', views.error_view, name='error'),
    path('cpu/', views.cpu_spike_view, name='cpu_spike'),
    path('memory/', views.memory_spike_view, name='memory_spike'),
    path('logs/', views.logs_view, name='logs'),
]