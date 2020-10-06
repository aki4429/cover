from django.urls import path
from . import views

urlpatterns = [
    path('', views.loc_list, name='loc_list'),
    path('loc/<int:pk>/', views.loc_detail, name='loc_detail'),
    path('loc/new/', views.loc_new, name='loc_new'),
    path('loc/<int:pk>/edit/', views.loc_edit, name='loc_edit'),
    path('loc/<pk>/remove/', views.loc_remove, name='loc_remove'),
    path('loc/<pk>/del/', views.loc_del, name='loc_del'),
    path('upload', views.model_form_upload, name='upload'),
    path('loc/shiji_list', views.shiji_list, name='shiji_list'),
    path('<int:shiji_id>/del/', views.shiji_del, name='shiji_del'),
    path('loc/seisan_list', views.seisan_list, name='seisan_list'),
    path('<int:shiji_id>/seisan/', views.make_seisan, name='make_seisan'),
    path('loc/pick_list', views.pick_list, name='pick_list'),
    path('loc/pick', views.make_pick, name='make_pick'),
    path('<int:pick_id>/koshin/', views.koshin, name='koshin'),
    path('<int:kaku_id>/rollback/', views.rollback, name='rollback'),
    path('loc/status/', views.status_edit, name='status_edit'),
    path('loc/download_pick/<int:pick_pk>', views.download_pick, name='download_pick'),
    path('loc/kaku_list', views.kaku_list, name='kaku_list'),
]
