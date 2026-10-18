"""Verificações analíticas independentes para figuras isoladas."""
from math import pi
import pytest
from geometria.retangulo import Retangulo
from geometria.circulo import Circulo
from geometria.semicirculo import Semicirculo
from geometria.quarto_circulo import QuartoCirculo
from geometria.triangulo import Triangulo
from geometria.poligono import Poligono


def test_retangulo_area_centroide_inercias():
    f = Retangulo(b=4, h=2)
    assert f.area() == pytest.approx(8)
    assert f.centroide() == pytest.approx((2, 1))
    assert f.inercias_centrais() == pytest.approx((8/3, 32/3, 0))


def test_circulo_area_centroide_inercias():
    f = Circulo(r=2, x0=5, y0=-3)
    assert f.area() == pytest.approx(4*pi)
    assert f.centroide() == pytest.approx((5, -3))
    assert f.inercias_centrais() == pytest.approx((4*pi, 4*pi, 0))


def test_semicirculo_area_centroide_inercias():
    f = Semicirculo(r=2)
    assert f.area() == pytest.approx(2*pi)
    assert f.centroide() == pytest.approx((0, 8/(3*pi)))
    assert f.inercias_centrais() == pytest.approx((16*(pi/8 - 8/(9*pi)), 2*pi, 0))


def test_quarto_circulo_area_centroide():
    f = QuartoCirculo(r=3)
    assert f.area() == pytest.approx(9*pi/4)
    assert f.centroide() == pytest.approx((4/pi, 4/pi))


def test_triangulo_produto_de_inercia_negativo():
    f = Triangulo((200, 0), (350, 0), (200, 300))
    assert f.area() == pytest.approx(22500)
    assert f.centroide() == pytest.approx((250, 100))
    assert f.inercias_centrais() == pytest.approx((112500000, 28125000, -28125000))


def test_triangulo_inverte_ordem_vertices_sem_mudar_resultados():
    a = Triangulo((200, 0), (350, 0), (200, 300))
    b = Triangulo((200, 300), (350, 0), (200, 0))
    assert a.inercias_centrais() == pytest.approx(b.inercias_centrais())


def test_poligono_retangular_equivalente():
    f = Poligono([(0, 0), (4, 0), (4, 2), (0, 2)])
    assert f.area() == pytest.approx(8)
    assert f.centroide() == pytest.approx((2, 1))
    assert f.inercias_centrais() == pytest.approx((8/3, 32/3, 0))


def test_rotacao_retangulo_90_graus():
    f = Retangulo(b=4, h=2, theta=90)
    ix, iy, ixy = f.inercias_centrais()
    assert ix == pytest.approx(32/3)
    assert iy == pytest.approx(8/3)
    assert ixy == pytest.approx(0, abs=1e-10)


def test_parametros_invalidos():
    with pytest.raises(ValueError):
        Retangulo(b=0, h=2)
    with pytest.raises(ValueError):
        Circulo(r=-1)
    with pytest.raises(ValueError):
        Triangulo((0, 0), (1, 1), (2, 2))
