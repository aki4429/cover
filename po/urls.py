from django.urls import path
from . import views
 
urlpatterns = [
    path('tfc_code', views.CodeList.as_view(), name='tfc_code'),
]
