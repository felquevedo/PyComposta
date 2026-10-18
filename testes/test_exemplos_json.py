"""Seis casos de regressão do PyComposta, com resultados de referência."""
import json
from pathlib import Path
import pytest
from geometria.retangulo import Retangulo
from geometria.circulo import Circulo
from geometria.semicirculo import Semicirculo
from geometria.quarto_circulo import QuartoCirculo
from geometria.triangulo import Triangulo
from geometria.poligono import Poligono
from geometria.secao_composta import SecaoComposta

DADOS = Path(__file__).parent / 'dados'
CLASSES = {
    'Retangulo': Retangulo,
    'Circulo': Circulo,
    'Semicirculo': Semicirculo,
    'QuartoCirculo': QuartoCirculo,
    'Triangulo': Triangulo,
    'Poligono': Poligono,
}

# Área, xc, yc, Ix, Iy, Ixy, Iu, Iv, angulo em graus.
# Valores arredondados obtidos na verificação anterior; as tolerâncias
# preservam os dígitos efetivamente publicados na tabela de referência.
REFERENCIAS = {
    1: (4159.016, 34.532, -1.252, 8.768e5, 3.450e6, -1.945e5, 3464486.183, 862151.992, -85.702),
    2: (64828.541, 152.060, 132.647, 5.744e8, 5.338e8, -1.383e8, 693884450.571, 414313059.911, -40.829),
    3: (120000.0, 0.0, 0.0, 2.900e9, 5.600e9, -3.000e9, 7539756829.919, 960243170.081, -57.114),
    4: (3493.142, 40.937, 29.941, 9.148e5, 1.507e6, 6.197e5, 1897612.894, 524073.631, 57.769),
    5: (13828.319, 54.793, 96.611, 3.425e7, 1.854e7, 4.796e6, 35594252.084, 17194852.673, 15.710),
    6: (75090.266, 166.025, 120.0, 6.119e8, 1.075e9, -4.147e8, 1318373156.794, 368448281.145, -59.586),
}


def carregar_exemplo(numero):
    with (DADOS / f'exemplo{numero}.json').open(encoding='utf-8') as arq:
        dados = json.load(arq)
    assert dados['formato'] == 'PyComposta'
    secao = SecaoComposta()
    for item in dados['figuras']:
        item = dict(item)
        tipo = item.pop('tipo')
        vertices = item.pop('vertices', None)
        if tipo == 'Triangulo':
            figura = Triangulo(*vertices, **item)
        elif tipo == 'Poligono':
            figura = Poligono(vertices, **item)
        else:
            figura = CLASSES[tipo](**item)
        secao.adicionar(figura)
    return secao


@pytest.mark.parametrize('numero', sorted(REFERENCIAS))
def test_seis_exemplos(numero):
    secao = carregar_exemplo(numero)
    esperado = REFERENCIAS[numero]
    a = secao.area()
    xc, yc = secao.centroide()
    ix, iy, ixy = secao.inercias_centrais()
    iu, iv, ang = secao.inercias_principais()
    obtidos = (a, xc, yc, ix, iy, ixy, iu, iv, ang)
    # Os valores de referência de Ix, Iy e Ixy foram publicados com 4 dígitos;
    # tolerância relativa de 0,1% somente nesses três campos arredondados.
    for indice, (valor, ref) in enumerate(zip(obtidos, esperado)):
        if indice in (3, 4, 5):
            assert valor == pytest.approx(ref, rel=1e-3, abs=1e-6), (numero, indice)
        elif indice in (0, 1, 2, 8):
            assert valor == pytest.approx(ref, abs=0.001, rel=0), (numero, indice)
        else:
            assert valor == pytest.approx(ref, abs=0.01, rel=0), (numero, indice)
    assert iu + iv == pytest.approx(ix + iy, rel=1e-12)
    assert iu * iv == pytest.approx(ix * iy - ixy**2, rel=1e-12)
    assert iu >= iv


def test_area_nao_positiva_gera_erro():
    secao = SecaoComposta([Circulo(r=2, sinal=-1)])
    with pytest.raises(ValueError):
        secao.centroide()
