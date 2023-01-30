from django.urls import path
from . import views


app_name = 'pedido'


urlpatterns = [
    path('pagar/', views.Pagar.as_view(), name='pagar'),
    path('fechar_pedido/', views.FecharPedido.as_view(), name='fechar_pedido'),
    path('detalhe/', views.Detalhe.as_view(), name='detalhe'),
    
]