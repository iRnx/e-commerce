from django.contrib import admin
from .models import Pedido, ItemPedido


class ItemPedidoInline(admin.StackedInline):
    model = ItemPedido
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [ItemPedidoInline]


admin.site.register(ItemPedido)
