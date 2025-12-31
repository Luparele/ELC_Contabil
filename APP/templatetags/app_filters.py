from django import template

register = template.Library()

@register.filter
def class_name(value):
    return value.__class__.__name__

# --- NOVO FILTRO ADICIONADO ---
@register.filter(name='format_currency')
def format_currency(value):
    """
    Formata um número para o padrão monetário brasileiro (ex: 1234.50 -> 1.234,50).
    """
    if value is None:
        value = 0
    # Usa f-string para formatar com 2 casas decimais e separador de milhar.
    # Depois, substitui os caracteres para o padrão brasileiro.
    return f'{value:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")

@register.filter(name='format_percent')
def format_percent(value, decimals=2):
    """
    Formata um número como porcentagem com um número específico de casas decimais.
    Mostra o valor mesmo que seja muito pequeno (ex: 0.01).
    """
    if value is None:
        value = 0
    # Usa uma f-string para formatar o número e substitui o ponto pela vírgula
    return f"{value:.{decimals}f}".replace('.', ',')