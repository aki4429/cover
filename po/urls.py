from django.urls import path
from . import views
 
urlpatterns = [
    path('tfc_code', views.CodeList.as_view(), name='tfc_code'),
    path('code_update/<int:pk>/', views.CodeUpdate.as_view(), name='code_update'),
    path('<int:pk>/code_detail/', views.CodeDetail.as_view(), name='code_detail'),
    path('code_create/', views.CodeCreate.as_view(), name='code_create'),
    path('<int:pk>/code_copy/', views.CodeCopy.as_view(), name='code_copy'),
    path('juchu_upload/', views.juchu_upload, name='juchu_upload'),
    path('juchu_list/', views.JuchuList.as_view(), name='juchu_list'),
    path('<int:pk>/code_delete/', views.CodeDelete.as_view(), name='code_delete'),
    path('<int:pk>/juchu_delete/', views.juchu_delete, name='juchu_delete'),
]
