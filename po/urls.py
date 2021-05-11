from django.urls import path
from . import views

urlpatterns = [
    path('tfc_code', views.CodeList.as_view(), name='tfc_code'),
    path('code_update/<int:pk>/', views.CodeUpdate.as_view(), name='code_update'),
    path('po_update/<int:pk>/', views.PoUpdate.as_view(), name='po_update'),
    path('cart_update/<int:pk>/', views.CartUpdate.as_view(), name='cart_update'),
    path('po_line/<int:pk>/', views.PolineUpdate.as_view(), name='poline_update'),
    path('<int:pk>/code_detail/', views.CodeDetail.as_view(), name='code_detail'),
    path('code_create/', views.CodeCreate.as_view(), name='code_create'),
    path('<int:condi_pk>/po_create/', views.PoCreate.as_view(), name='po_create'),
    path('<int:pk>/code_copy/', views.CodeCopy.as_view(), name='code_copy'),
    path('juchu_upload/', views.juchu_upload, name='juchu_upload'),
    path('kento_upload/', views.kento_upload, name='kento_upload'),
    path('juchu_list/', views.JuchuList.as_view(), name='juchu_list'),
    path('po_list/', views.PoList.as_view(), name='po_list'),
    path('<int:po_pk>/poline_list/', views.PolineList.as_view(), name='poline_list'),
    path('<int:juchu_id>/make_cart/', views.make_cart, name='make_cart'),
    path('<int:pk>/cart_apend/', views.cart_append, name='cart_append'),
    path('cart_list/', views.CartList.as_view(), name='cart_list'),
    path('<int:pk>/cart_delete/', views.CartDelete.as_view(), name='cart_delete'),
    path('<int:pk>/code_delete/', views.CodeDelete.as_view(), name='code_delete'),
    path('<int:pk>/po_delete/', views.PoDelete.as_view(), name='po_delete'),
    path('<int:pk>/poline_delete/', views.PolineDelete.as_view(), name='poline_delete'),
    path('<int:pk>/juchu_delete/', views.juchu_delete, name='juchu_delete'),
    path('cart_delete_all/', views.cart_delete_all, name='cart_delete_all'),
    path('order_list/', views.order_list, name='order_list'),
    path('condition_list/', views.ConditionList.as_view(), name='condition_list'),
    path('make_po/<int:po_pk>/', views.make_po, name='make_po'),
    path('add_order/<int:po_pk>/', views.add_order, name='add_order'),
    path('condition_update/<int:pk>/', views.ConditionUpdate.as_view(), name='condition_update'),
    path('<int:pk>/condition_copy/', views.ConditionCopy.as_view(), name='condition_copy'),
    path('<int:pk>/condition_delete/', views.ConditionDelete.as_view(), name='condition_delete'),
]
