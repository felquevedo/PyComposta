"""Casos originais de secao_composta, migrados de __main__ sem alterar as asserções."""
from geometria.secao_composta import *
from math import isclose, pi
from geometria.retangulo import Retangulo
from geometria.circulo import Circulo
from geometria.semicirculo import Semicirculo
from geometria.triangulo import Triangulo
def verificar(valor, esperado):
    assert isclose(
        valor, esperado,
        rel_tol=1e-8,
        abs_tol=1e-7
    ), f"Esperado {esperado}, obtido {valor}"


def test_original_01():
    secao = SecaoComposta([
        Retangulo(b=2, h=4),
        Retangulo(b=2, h=4, x0=2)
    ])
    verificar(secao.area(), 16)
    xc, yc = secao.centroide()
    verificar(xc, 2)
    verificar(yc, 2)
    Ix, Iy, Ixy = secao.inercias_centrais()
    verificar(Ix, 4*4**3/12)
    verificar(Iy, 4*4**3/12)
    verificar(Ixy, 0)


def test_original_02():
    secao = SecaoComposta([
        Retangulo(b=2, h=4),
        Retangulo(b=2, h=4, x0=2)
    ])
    verificar(secao.area(), 16)
    xc, yc = secao.centroide()
    verificar(xc, 2)
    verificar(yc, 2)
    Ix, Iy, Ixy = secao.inercias_centrais()
    verificar(Ix, 4*4**3/12)
    verificar(Iy, 4*4**3/12)
    verificar(Ixy, 0)
    secao = SecaoComposta([
        Retangulo(b=10, h=6),
        Circulo(r=2, x0=5, y0=3, sinal=-1)
    ])
    verificar(secao.area(), 60-4*pi)
    xc, yc = secao.centroide()
    verificar(xc, 5)
    verificar(yc, 3)
    Ix, Iy, Ixy = secao.inercias_centrais()
    verificar(Ix, 10*6**3/12-4*pi)
    verificar(Iy, 6*10**3/12-4*pi)
    verificar(Ixy, 0)


def test_original_03():
    secao = SecaoComposta([
        Retangulo(b=2, h=4),
        Retangulo(b=2, h=4, x0=2)
    ])
    verificar(secao.area(), 16)
    xc, yc = secao.centroide()
    verificar(xc, 2)
    verificar(yc, 2)
    Ix, Iy, Ixy = secao.inercias_centrais()
    verificar(Ix, 4*4**3/12)
    verificar(Iy, 4*4**3/12)
    verificar(Ixy, 0)
    secao = SecaoComposta([
        Retangulo(b=10, h=6),
        Circulo(r=2, x0=5, y0=3, sinal=-1)
    ])
    verificar(secao.area(), 60-4*pi)
    xc, yc = secao.centroide()
    verificar(xc, 5)
    verificar(yc, 3)
    Ix, Iy, Ixy = secao.inercias_centrais()
    verificar(Ix, 10*6**3/12-4*pi)
    verificar(Iy, 6*10**3/12-4*pi)
    verificar(Ixy, 0)
    exemplo = SecaoComposta([
        Retangulo(
            b=120, h=140
        ),
        Triangulo(
            (0, 0), (120, 0), (120, 60),
            sinal=-1
        ),
        Semicirculo(
            r=60, x0=60, y0=140
        ),
        Circulo(
            r=40, x0=60, y0=140,
            sinal=-1
        )
    ])
    verificar(exemplo.area(), 13200+200*pi)
    xc, yc = exemplo.centroide()
    verificar(xc, 54.7932932091)
    verificar(yc, 96.6107767429)
    Ix, Iy, Ixy = exemplo.inercias_centrais()
    verificar(Ix, 34245226.846241)
    verificar(Iy, 18543877.911576)
    verificar(Ixy, 4795975.925487)


def test_original_04():
    secao = SecaoComposta([
        Retangulo(b=2, h=4),
        Retangulo(b=2, h=4, x0=2)
    ])
    verificar(secao.area(), 16)
    xc, yc = secao.centroide()
    verificar(xc, 2)
    verificar(yc, 2)
    Ix, Iy, Ixy = secao.inercias_centrais()
    verificar(Ix, 4*4**3/12)
    verificar(Iy, 4*4**3/12)
    verificar(Ixy, 0)
    secao = SecaoComposta([
        Retangulo(b=10, h=6),
        Circulo(r=2, x0=5, y0=3, sinal=-1)
    ])
    verificar(secao.area(), 60-4*pi)
    xc, yc = secao.centroide()
    verificar(xc, 5)
    verificar(yc, 3)
    Ix, Iy, Ixy = secao.inercias_centrais()
    verificar(Ix, 10*6**3/12-4*pi)
    verificar(Iy, 6*10**3/12-4*pi)
    verificar(Ixy, 0)
    exemplo = SecaoComposta([
        Retangulo(
            b=120, h=140
        ),
        Triangulo(
            (0, 0), (120, 0), (120, 60),
            sinal=-1
        ),
        Semicirculo(
            r=60, x0=60, y0=140
        ),
        Circulo(
            r=40, x0=60, y0=140,
            sinal=-1
        )
    ])
    verificar(exemplo.area(), 13200+200*pi)
    xc, yc = exemplo.centroide()
    verificar(xc, 54.7932932091)
    verificar(yc, 96.6107767429)
    Ix, Iy, Ixy = exemplo.inercias_centrais()
    verificar(Ix, 34245226.846241)
    verificar(Iy, 18543877.911576)
    verificar(Ixy, 4795975.925487)
    Imax, Imin, angulo = (
        exemplo.inercias_principais()
    )
    verificar(Imax, 35594252.084327)
    verificar(Imin, 17194852.673491)
    verificar(angulo, 15.7103760472)
    Iu, Iv, Iuv = exemplo.inercias_eixos(
        xp=xc, yp=yc, angulo=angulo
    )
    verificar(Iu, Imax)
    verificar(Iv, Imin)
    verificar(Iuv, 0)

