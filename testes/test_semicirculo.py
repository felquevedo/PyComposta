"""Testes de semicirculo.

Cada teste documenta o objetivo do caso e compara valores numericos
com resultados de referencia usando a funcao verificar.
Os cenarios migrados mantem verificacoes acumuladas do codigo original.
"""
from geometria.semicirculo import *
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
    s1 = Semicirculo(r=2)
    verificar(s1.area(), 2*pi)
    xc, yc = s1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = s1.inercias_centrais()
    verificar(Ix, 16*(pi/8 - 8/(9*pi)))
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)


def test_inercia_apos_rotacao():
    """Verifica inercia apos rotacao.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    s1 = Semicirculo(r=2)
    verificar(s1.area(), 2*pi)
    xc, yc = s1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = s1.inercias_centrais()
    verificar(Ix, 16*(pi/8 - 8/(9*pi)))
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = s1.inercias_origem()
    verificar(Ix, 2*pi)
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)


def test_centroide_apos_translacao_e_rotacao():
    """Verifica centroide apos translacao e rotacao.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    s1 = Semicirculo(r=2)
    verificar(s1.area(), 2*pi)
    xc, yc = s1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = s1.inercias_centrais()
    verificar(Ix, 16*(pi/8 - 8/(9*pi)))
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = s1.inercias_origem()
    verificar(Ix, 2*pi)
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)
    s2 = Semicirculo(
        r=2, x0=3, y0=1, theta=90
    )
    xc, yc = s2.centroide()
    verificar(xc, 3 - 8/(3*pi))
    verificar(yc, 1.0)
    Ix, Iy, Ixy = s2.inercias_centrais()
    verificar(Ix, 2*pi)
    verificar(Iy, 16*(pi/8 - 8/(9*pi)))
    verificar(Ixy, 0.0)


def test_momentos_principais_do_semicirculo():
    """Verifica momentos principais do semicirculo.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    s1 = Semicirculo(r=2)
    verificar(s1.area(), 2*pi)
    xc, yc = s1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = s1.inercias_centrais()
    verificar(Ix, 16*(pi/8 - 8/(9*pi)))
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = s1.inercias_origem()
    verificar(Ix, 2*pi)
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)
    s2 = Semicirculo(
        r=2, x0=3, y0=1, theta=90
    )
    xc, yc = s2.centroide()
    verificar(xc, 3 - 8/(3*pi))
    verificar(yc, 1.0)
    Ix, Iy, Ixy = s2.inercias_centrais()
    verificar(Ix, 2*pi)
    verificar(Iy, 16*(pi/8 - 8/(9*pi)))
    verificar(Ixy, 0.0)
    Imax, Imin, angulo = s1.inercias_principais()
    verificar(Imax, 2*pi)
    verificar(Imin, 16*(pi/8 - 8/(9*pi)))
    verificar(angulo, -90.0)


def test_rejeicao_de_raios_invalidos():
    """Verifica rejeicao de raios invalidos.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    s1 = Semicirculo(r=2)
    verificar(s1.area(), 2*pi)
    xc, yc = s1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = s1.inercias_centrais()
    verificar(Ix, 16*(pi/8 - 8/(9*pi)))
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = s1.inercias_origem()
    verificar(Ix, 2*pi)
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)
    s2 = Semicirculo(
        r=2, x0=3, y0=1, theta=90
    )
    xc, yc = s2.centroide()
    verificar(xc, 3 - 8/(3*pi))
    verificar(yc, 1.0)
    Ix, Iy, Ixy = s2.inercias_centrais()
    verificar(Ix, 2*pi)
    verificar(Iy, 16*(pi/8 - 8/(9*pi)))
    verificar(Ixy, 0.0)
    Imax, Imin, angulo = s1.inercias_principais()
    verificar(Imax, 2*pi)
    verificar(Imin, 16*(pi/8 - 8/(9*pi)))
    verificar(angulo, -90.0)
    for r in (-2, 0):
        try:
            Semicirculo(r)
        except ValueError:
            pass
        else:
            raise AssertionError("Era esperado ValueError.")
    vazado = Semicirculo(r=2, sinal=-1)
    verificar(vazado.area(), 2*pi)
    assert vazado.sinal == -1

