from django.urls import path
from . import views

urlpatterns = [
    path('', views.loc_list, name='loc_list'),
    path('loc/<int:pk>/', views.loc_detail, name='loc_detail'),
    path('loc/new/', views.loc_new, name='loc_new'),
    path('loc/<int:pk>/edit/', views.loc_edit, name='loc_edit'),
    path('loc/<pk>/remove/', views.loc_remove, name='loc_remove'),
    path('loc/<pk>/del/', views.loc_del, name='loc_del'),
    path('upload', views.model_form_upload, name='upload')
]
