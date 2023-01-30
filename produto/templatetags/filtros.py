from django.template import Library
from utils import utils


register = Library()


@register.filter(name='preco_formatado')
def formata_preco(value):
    return utils.formata_preco(value)