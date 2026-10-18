"""Testes de quarto circulo.

Cada teste documenta o objetivo do caso e compara valores numericos
com resultados de referencia usando a funcao verificar.
Os cenarios migrados mantem verificacoes acumuladas do codigo original.
"""
from geometria.quarto_circulo import *
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
    q1 = QuartoCirculo(r=2)
    verificar(q1.area(), pi)
    xc, yc = q1.centroide()
    verificar(xc, 8/(3*pi))
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = q1.inercias_centrais()
    verificar(Ix, 16*(pi/16 - 4/(9*pi)))
    verificar(Iy, 16*(pi/16 - 4/(9*pi)))
    verificar(Ixy, 16*(1/8 - 4/(9*pi)))


def test_produto_de_inercia_do_quarto_de_circulo():
    """Verifica produto de inercia do quarto de circulo.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    q1 = QuartoCirculo(r=2)
    verificar(q1.area(), pi)
    xc, yc = q1.centroide()
    verificar(xc, 8/(3*pi))
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = q1.inercias_centrais()
    verificar(Ix, 16*(pi/16 - 4/(9*pi)))
    verificar(Iy, 16*(pi/16 - 4/(9*pi)))
    verificar(Ixy, 16*(1/8 - 4/(9*pi)))
    Ix, Iy, Ixy = q1.inercias_origem()
    verificar(Ix, pi)
    verificar(Iy, pi)
    verificar(Ixy, 2.0)


def test_rotacao_de_90_graus():
    """Verifica rotacao de 90 graus.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    q1 = QuartoCirculo(r=2)
    verificar(q1.area(), pi)
    xc, yc = q1.centroide()
    verificar(xc, 8/(3*pi))
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = q1.inercias_centrais()
    verificar(Ix, 16*(pi/16 - 4/(9*pi)))
    verificar(Iy, 16*(pi/16 - 4/(9*pi)))
    verificar(Ixy, 16*(1/8 - 4/(9*pi)))
    Ix, Iy, Ixy = q1.inercias_origem()
    verificar(Ix, pi)
    verificar(Iy, pi)
    verificar(Ixy, 2.0)
    q2 = QuartoCirculo(
        r=2,
        x0=3,
        y0=1,
        theta=90
    )
    xc, yc = q2.centroide()
    verificar(xc, 3 - 8/(3*pi))
    verificar(yc, 1 + 8/(3*pi))
    Ix, Iy, Ixy = q2.inercias_centrais()
    Icentral = 16*(pi/16 - 4/(9*pi))
    Pcentral = 16*(1/8 - 4/(9*pi))
    verificar(Ix, Icentral)
    verificar(Iy, Icentral)
    verificar(Ixy, -Pcentral)


def test_momentos_principais():
    """Verifica momentos principais.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    q1 = QuartoCirculo(r=2)
    verificar(q1.area(), pi)
    xc, yc = q1.centroide()
    verificar(xc, 8/(3*pi))
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = q1.inercias_centrais()
    verificar(Ix, 16*(pi/16 - 4/(9*pi)))
    verificar(Iy, 16*(pi/16 - 4/(9*pi)))
    verificar(Ixy, 16*(1/8 - 4/(9*pi)))
    Ix, Iy, Ixy = q1.inercias_origem()
    verificar(Ix, pi)
    verificar(Iy, pi)
    verificar(Ixy, 2.0)
    q2 = QuartoCirculo(
        r=2,
        x0=3,
        y0=1,
        theta=90
    )
    xc, yc = q2.centroide()
    verificar(xc, 3 - 8/(3*pi))
    verificar(yc, 1 + 8/(3*pi))
    Ix, Iy, Ixy = q2.inercias_centrais()
    Icentral = 16*(pi/16 - 4/(9*pi))
    Pcentral = 16*(1/8 - 4/(9*pi))
    verificar(Ix, Icentral)
    verificar(Iy, Icentral)
    verificar(Ixy, -Pcentral)
    Imax, Imin, angulo = q1.inercias_principais()
    Icentral = 16*(pi/16 - 4/(9*pi))
    Pcentral = 16*(1/8 - 4/(9*pi))
    verificar(Imax, Icentral - Pcentral)
    verificar(Imin, Icentral + Pcentral)
    verificar(angulo, -45.0)


def test_transformacao_para_eixos_rotacionados():
    """Verifica transformacao para eixos rotacionados.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    q1 = QuartoCirculo(r=2)
    verificar(q1.area(), pi)
    xc, yc = q1.centroide()
    verificar(xc, 8/(3*pi))
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = q1.inercias_centrais()
    verificar(Ix, 16*(pi/16 - 4/(9*pi)))
    verificar(Iy, 16*(pi/16 - 4/(9*pi)))
    verificar(Ixy, 16*(1/8 - 4/(9*pi)))
    Ix, Iy, Ixy = q1.inercias_origem()
    verificar(Ix, pi)
    verificar(Iy, pi)
    verificar(Ixy, 2.0)
    q2 = QuartoCirculo(
        r=2,
        x0=3,
        y0=1,
        theta=90
    )
    xc, yc = q2.centroide()
    verificar(xc, 3 - 8/(3*pi))
    verificar(yc, 1 + 8/(3*pi))
    Ix, Iy, Ixy = q2.inercias_centrais()
    Icentral = 16*(pi/16 - 4/(9*pi))
    Pcentral = 16*(1/8 - 4/(9*pi))
    verificar(Ix, Icentral)
    verificar(Iy, Icentral)
    verificar(Ixy, -Pcentral)
    Imax, Imin, angulo = q1.inercias_principais()
    Icentral = 16*(pi/16 - 4/(9*pi))
    Pcentral = 16*(1/8 - 4/(9*pi))
    verificar(Imax, Icentral - Pcentral)
    verificar(Imin, Icentral + Pcentral)
    verificar(angulo, -45.0)
    xc, yc = q1.centroide()
    Iu, Iv, Iuv = q1.inercias_eixos(
        xp=xc,
        yp=yc,
        angulo=45
    )
    verificar(Iu, Icentral + Pcentral)
    verificar(Iv, Icentral - Pcentral)
    verificar(Iuv, 0.0)


def test_raios_invalidos_e_figura_vazada():
    """Verifica raios invalidos e figura vazada.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    q1 = QuartoCirculo(r=2)
    verificar(q1.area(), pi)
    xc, yc = q1.centroide()
    verificar(xc, 8/(3*pi))
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = q1.inercias_centrais()
    verificar(Ix, 16*(pi/16 - 4/(9*pi)))
    verificar(Iy, 16*(pi/16 - 4/(9*pi)))
    verificar(Ixy, 16*(1/8 - 4/(9*pi)))
    Ix, Iy, Ixy = q1.inercias_origem()
    verificar(Ix, pi)
    verificar(Iy, pi)
    verificar(Ixy, 2.0)
    q2 = QuartoCirculo(
        r=2,
        x0=3,
        y0=1,
        theta=90
    )
    xc, yc = q2.centroide()
    verificar(xc, 3 - 8/(3*pi))
    verificar(yc, 1 + 8/(3*pi))
    Ix, Iy, Ixy = q2.inercias_centrais()
    Icentral = 16*(pi/16 - 4/(9*pi))
    Pcentral = 16*(1/8 - 4/(9*pi))
    verificar(Ix, Icentral)
    verificar(Iy, Icentral)
    verificar(Ixy, -Pcentral)
    Imax, Imin, angulo = q1.inercias_principais()
    Icentral = 16*(pi/16 - 4/(9*pi))
    Pcentral = 16*(1/8 - 4/(9*pi))
    verificar(Imax, Icentral - Pcentral)
    verificar(Imin, Icentral + Pcentral)
    verificar(angulo, -45.0)
    xc, yc = q1.centroide()
    Iu, Iv, Iuv = q1.inercias_eixos(
        xp=xc,
        yp=yc,
        angulo=45
    )
    verificar(Iu, Icentral + Pcentral)
    verificar(Iv, Icentral - Pcentral)
    verificar(Iuv, 0.0)
    for r in (-2, 0):
        try:
            QuartoCirculo(r)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Era esperado ValueError."
            )
    vazado = QuartoCirculo(r=2, sinal=-1)
    verificar(vazado.area(), pi)
    assert vazado.sinal == -1

