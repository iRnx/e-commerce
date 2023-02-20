from django.db import models
from stdimage.models import StdImageField
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from utils import utils



class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = StdImageField(upload_to='fotos/%Y/%m/%d', variations={'thumbnail': {'width': 700, 'height': 500}}, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(default='V', max_length=1 ,choices=( ('V', 'Variável'), ('S', 'Simples') ))

    def __str__(self) -> str:
        return self.nome

    

    def get_preco_formatado(self):
        return utils.formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'


    def get_preco_promocional_formatado(self):
        return utils.formata_preco(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preço Promocional'


    @mark_safe
    def img(self):
        return f'<img src="/media/{self.imagem.thumbnail}" width="30px">'


    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        return super().save(*args, **kwargs)


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    def __str__(self) -> str:
        return self.nome or self.produto.nome

