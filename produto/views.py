from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from pprint import pprint
from . import models

from pprint import pprint


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'
    


# Trata-se de um formulario
class AdicionarCarrinho(View):

    def get(self, *args, **kwargs):

        # if self.request.session.get('carrinho'):
        #     del self.request.session['carrinho']
        #     self.request.session.save()

        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')


        print(self.request.POST)

        if not variacao_id:
            messages.error(self.request, 'Produto não existe')
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional

        quantidade = 1

        produto = variacao.produto
        produto_id = produto.id
        produto_nome = produto.nome
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''


        if variacao.estoque < 1:
            messages.error(self.request, 'Estoque insuficiente')
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()


        if variacao_id in self.request.session['carrinho']:
            quantidade_carrinho = self.request.session['carrinho'][variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(self.request, f'Estoque insuficiente para {quantidade_carrinho}x no produto "{produto.nome}". Adicionamos {variacao_estoque}x no seu carrinho')
                quantidade_carrinho = variacao_estoque

            self.request.session['carrinho'][variacao_id]['quantidade'] = quantidade_carrinho
            self.request.session['carrinho'][variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            self.request.session['carrinho'][variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho
            

        else:
            # TODO: Variação não existe no carrinho
            self.request.session['carrinho'][variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome, 
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id, 
                'preco_unitario': preco_unitario, 
                'preco_unitario_promocional': preco_unitario_promocional, 
                'preco_quantitativo': preco_unitario, 
                'preco_quantitativo_promocional': preco_unitario_promocional, 
                'quantidade': 1,
                'slug': slug, 
                'imagem': imagem, 
            }

        carrinho = self.request.session['carrinho']
        self.request.session.save()
        pprint(self.request.session['carrinho'])
        messages.success(self.request, f'"{produto_nome} {variacao_nome}" Adicionado ao seu Carrinho {carrinho[variacao_id]["quantidade"]}x')
        return redirect(http_referer)


        return HttpResponse(f'{variacao.produto} {variacao.nome}')


class RemoverCarrinho(View):
    def get(self, *args, **kwargs):

        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)
        
        carrinho = self.request.session['carrinho'][variacao_id]

        messages.success(self.request, f'Produto {carrinho["produto_nome"]} {carrinho["variacao_nome"]} removido do seu carrinho')

        # Removendo do carrinho
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)

class Carrinho(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'produto/carrinho.html')


class Finalizar(View):
    pass

