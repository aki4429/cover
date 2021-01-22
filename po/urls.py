from django.urls import path
from . import views
 
urlpatterns = [
    path('tfc_code', views.CodeList.as_view(), name='tfc_code'),
    path('code_update/<int:pk>/', views.CodeUpdate.as_view(), name='code_update'),
    path('<int:pk>/code_detail/', views.CodeDetail.as_view(), name='code_detail'),
]
