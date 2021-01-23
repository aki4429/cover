from django.urls import path
from . import views
 
urlpatterns = [
    path('tfc_code', views.CodeList.as_view(), name='tfc_code'),
    path('code_update/<int:pk>/', views.CodeUpdate.as_view(), name='code_update'),
    path('<int:pk>/code_detail/', views.CodeDetail.as_view(), name='code_detail'),
    path('code_create/', views.CodeCreate.as_view(), name='code_create'),
    path('<int:pk>/code_copy/', views.CodeCopy.as_view(), name='code_copy'),
]
