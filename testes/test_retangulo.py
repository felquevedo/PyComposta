"""Testes de retangulo.

Cada teste documenta o objetivo do caso e compara valores numericos
com resultados de referencia usando a funcao verificar.
Os cenarios migrados mantem verificacoes acumuladas do codigo original.
"""
from geometria.retangulo import *
def verificar(valor, esperado):
    """Compara resultado e referencia com tolerancias numericas."""
    assert isclose(
        valor, esperado,
        rel_tol=1e-9,
        abs_tol=1e-9
    ), f"Esperado {esperado}, obtido {valor}"


def test_area_centroide_e_inercias_basicas():
    """Verifica area centroide e inercias basicas.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    r1 = Retangulo(b=4, h=2)
    verificar(r1.area(), 8.0)
    xc, yc = r1.centroide()
    verificar(xc, 2.0)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = r1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = r1.inercias_origem()
    verificar(Ix, 32/3)
    verificar(Iy, 128/3)
    verificar(Ixy, 16.0)


def test_translacao_e_rotacao_30_graus():
    """Verifica translacao e rotacao 30 graus.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    r1 = Retangulo(b=4, h=2)
    verificar(r1.area(), 8.0)
    xc, yc = r1.centroide()
    verificar(xc, 2.0)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = r1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = r1.inercias_origem()
    verificar(Ix, 32/3)
    verificar(Iy, 128/3)
    verificar(Ixy, 16.0)
    r2 = Retangulo(
        b=4,
        h=2,
        x0=3,
        y0=1,
        theta=30
    )
    verificar(r2.area(), 8.0)
    xc, yc = r2.centroide()
    verificar(xc, 4.232050807568877)
    verificar(yc, 2.8660254037844384)
    Ix, Iy, Ixy = r2.inercias_centrais()
    verificar(Ix, 4.666666666666667)
    verificar(Iy, 8.666666666666666)
    verificar(Ixy, -3.4641016151377544)


def test_momentos_principais_do_retangulo_rotacionado():
    """Verifica momentos principais do retangulo rotacionado.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    r1 = Retangulo(b=4, h=2)
    verificar(r1.area(), 8.0)
    xc, yc = r1.centroide()
    verificar(xc, 2.0)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = r1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = r1.inercias_origem()
    verificar(Ix, 32/3)
    verificar(Iy, 128/3)
    verificar(Ixy, 16.0)
    r2 = Retangulo(
        b=4,
        h=2,
        x0=3,
        y0=1,
        theta=30
    )
    verificar(r2.area(), 8.0)
    xc, yc = r2.centroide()
    verificar(xc, 4.232050807568877)
    verificar(yc, 2.8660254037844384)
    Ix, Iy, Ixy = r2.inercias_centrais()
    verificar(Ix, 4.666666666666667)
    verificar(Iy, 8.666666666666666)
    verificar(Ixy, -3.4641016151377544)
    Imax, Imin, angulo = r2.inercias_principais()
    verificar(Imax, 32/3)
    verificar(Imin, 8/3)
    verificar(angulo, -60.0)


def test_transformacao_de_inercias_para_outros_eixos():
    """Verifica transformacao de inercias para outros eixos.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    r1 = Retangulo(b=4, h=2)
    verificar(r1.area(), 8.0)
    xc, yc = r1.centroide()
    verificar(xc, 2.0)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = r1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = r1.inercias_origem()
    verificar(Ix, 32/3)
    verificar(Iy, 128/3)
    verificar(Ixy, 16.0)
    r2 = Retangulo(
        b=4,
        h=2,
        x0=3,
        y0=1,
        theta=30
    )
    verificar(r2.area(), 8.0)
    xc, yc = r2.centroide()
    verificar(xc, 4.232050807568877)
    verificar(yc, 2.8660254037844384)
    Ix, Iy, Ixy = r2.inercias_centrais()
    verificar(Ix, 4.666666666666667)
    verificar(Iy, 8.666666666666666)
    verificar(Ixy, -3.4641016151377544)
    Imax, Imin, angulo = r2.inercias_principais()
    verificar(Imax, 32/3)
    verificar(Imin, 8/3)
    verificar(angulo, -60.0)
    Iu, Iv, Iuv = r2.inercias_eixos(
        xp=xc,
        yp=yc,
        angulo=30
    )
    verificar(Iu, 8/3)
    verificar(Iv, 32/3)
    verificar(Iuv, 0.0)
    Iu, Iv, Iuv = r1.inercias_eixos()
    verificar(Iu, 32/3)
    verificar(Iv, 128/3)
    verificar(Iuv, 16.0)


def test_rejeicao_de_dimensoes_invalidas():
    """Verifica rejeicao de dimensoes invalidas.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    r1 = Retangulo(b=4, h=2)
    verificar(r1.area(), 8.0)
    xc, yc = r1.centroide()
    verificar(xc, 2.0)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = r1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = r1.inercias_origem()
    verificar(Ix, 32/3)
    verificar(Iy, 128/3)
    verificar(Ixy, 16.0)
    r2 = Retangulo(
        b=4,
        h=2,
        x0=3,
        y0=1,
        theta=30
    )
    verificar(r2.area(), 8.0)
    xc, yc = r2.centroide()
    verificar(xc, 4.232050807568877)
    verificar(yc, 2.8660254037844384)
    Ix, Iy, Ixy = r2.inercias_centrais()
    verificar(Ix, 4.666666666666667)
    verificar(Iy, 8.666666666666666)
    verificar(Ixy, -3.4641016151377544)
    Imax, Imin, angulo = r2.inercias_principais()
    verificar(Imax, 32/3)
    verificar(Imin, 8/3)
    verificar(angulo, -60.0)
    Iu, Iv, Iuv = r2.inercias_eixos(
        xp=xc,
        yp=yc,
        angulo=30
    )
    verificar(Iu, 8/3)
    verificar(Iv, 32/3)
    verificar(Iuv, 0.0)
    Iu, Iv, Iuv = r1.inercias_eixos()
    verificar(Iu, 32/3)
    verificar(Iv, 128/3)
    verificar(Iuv, 16.0)
    for b, h in [(-4, 2), (4, -2), (0, 2)]:
        try:
            Retangulo(b=b, h=h)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Era esperado ValueError."
            )
    r3 = Retangulo(b=4, h=2, sinal=-1)
    verificar(r3.area(), 8.0)
    assert r3.sinal == -1

