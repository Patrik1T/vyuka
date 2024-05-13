from django.urls import path
from . import views

urlpatterns = [
    # cesta (route) pro zobrazení úvodní stránky
    path('', views.index, name='index'),
]