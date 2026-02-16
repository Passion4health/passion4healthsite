from django.urls import path
from .views import scholars_program_overview

urlpatterns = [
    path('', scholars_program_overview, name='scholars_program_overview'),
]
