from django.urls import path
from . import views

urlpatterns = [
    path('', views.loc_list, name='loc_list'),
]
