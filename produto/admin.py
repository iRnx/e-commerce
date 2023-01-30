from django.contrib import admin
from .models import Produto, Variacao


class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    inlines = [VariacaoInline]
    list_display = ('img', 'nome', 'descricao_curta', 'slug', 'get_preco_formatado', 'get_preco_promocional_formatado', 'tipo',)


admin.site.register(Variacao)
