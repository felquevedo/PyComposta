"""Testes de circulo.

Cada teste documenta o objetivo do caso e compara valores numericos
com resultados de referencia usando a funcao verificar.
Os cenarios migrados mantem verificacoes acumuladas do codigo original.
"""
from geometria.circulo import *
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
    c1 = Circulo(r=2)
    verificar(c1.area(), 4*pi)
    xc, yc = c1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 0.0)
    Ix, Iy, Ixy = c1.inercias_centrais()
    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)


def test_translacao_e_rotacao_sem_alterar_inercias():
    """Verifica translacao e rotacao sem alterar inercias.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    c1 = Circulo(r=2)
    verificar(c1.area(), 4*pi)
    xc, yc = c1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 0.0)
    Ix, Iy, Ixy = c1.inercias_centrais()
    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)
    c2 = Circulo(
        r=2,
        x0=3,
        y0=4,
        theta=30
    )
    verificar(c2.area(), 4*pi)
    xc, yc = c2.centroide()
    verificar(xc, 3.0)
    verificar(yc, 4.0)
    Ix, Iy, Ixy = c2.inercias_centrais()
    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)


def test_inercias_em_relacao_a_origem():
    """Verifica inercias em relacao a origem.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    c1 = Circulo(r=2)
    verificar(c1.area(), 4*pi)
    xc, yc = c1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 0.0)
    Ix, Iy, Ixy = c1.inercias_centrais()
    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)
    c2 = Circulo(
        r=2,
        x0=3,
        y0=4,
        theta=30
    )
    verificar(c2.area(), 4*pi)
    xc, yc = c2.centroide()
    verificar(xc, 3.0)
    verificar(yc, 4.0)
    Ix, Iy, Ixy = c2.inercias_centrais()
    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = c2.inercias_origem()
    verificar(Ix, 68*pi)
    verificar(Iy, 40*pi)
    verificar(Ixy, 48*pi)


def test_momentos_principais_do_circulo():
    """Verifica momentos principais do circulo.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    c1 = Circulo(r=2)
    verificar(c1.area(), 4*pi)
    xc, yc = c1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 0.0)
    Ix, Iy, Ixy = c1.inercias_centrais()
    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)
    c2 = Circulo(
        r=2,
        x0=3,
        y0=4,
        theta=30
    )
    verificar(c2.area(), 4*pi)
    xc, yc = c2.centroide()
    verificar(xc, 3.0)
    verificar(yc, 4.0)
    Ix, Iy, Ixy = c2.inercias_centrais()
    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = c2.inercias_origem()
    verificar(Ix, 68*pi)
    verificar(Iy, 40*pi)
    verificar(Ixy, 48*pi)
    Imax, Imin, angulo = c2.inercias_principais()
    verificar(Imax, 4*pi)
    verificar(Imin, 4*pi)
    verificar(angulo, 0.0)


def test_transformacao_de_inercias_para_outros_eixos():
    """Verifica transformacao de inercias para outros eixos.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    c1 = Circulo(r=2)
    verificar(c1.area(), 4*pi)
    xc, yc = c1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 0.0)
    Ix, Iy, Ixy = c1.inercias_centrais()
    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)
    c2 = Circulo(
        r=2,
        x0=3,
        y0=4,
        theta=30
    )
    verificar(c2.area(), 4*pi)
    xc, yc = c2.centroide()
    verificar(xc, 3.0)
    verificar(yc, 4.0)
    Ix, Iy, Ixy = c2.inercias_centrais()
    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = c2.inercias_origem()
    verificar(Ix, 68*pi)
    verificar(Iy, 40*pi)
    verificar(Ixy, 48*pi)
    Imax, Imin, angulo = c2.inercias_principais()
    verificar(Imax, 4*pi)
    verificar(Imin, 4*pi)
    verificar(angulo, 0.0)
    Iu, Iv, Iuv = c2.inercias_eixos(
        xp=3,
        yp=4,
        angulo=45
    )
    verificar(Iu, 4*pi)
    verificar(Iv, 4*pi)
    verificar(Iuv, 0.0)
    Iu, Iv, Iuv = c2.inercias_eixos()
    verificar(Iu, 68*pi)
    verificar(Iv, 40*pi)
    verificar(Iuv, 48*pi)


def test_rejeicao_de_raios_invalidos_e_circulo_vazado():
    """Verifica rejeicao de raios invalidos e circulo vazado.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    c1 = Circulo(r=2)
    verificar(c1.area(), 4*pi)
    xc, yc = c1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 0.0)
    Ix, Iy, Ixy = c1.inercias_centrais()
    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)
    c2 = Circulo(
        r=2,
        x0=3,
        y0=4,
        theta=30
    )
    verificar(c2.area(), 4*pi)
    xc, yc = c2.centroide()
    verificar(xc, 3.0)
    verificar(yc, 4.0)
    Ix, Iy, Ixy = c2.inercias_centrais()
    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)
    Ix, Iy, Ixy = c2.inercias_origem()
    verificar(Ix, 68*pi)
    verificar(Iy, 40*pi)
    verificar(Ixy, 48*pi)
    Imax, Imin, angulo = c2.inercias_principais()
    verificar(Imax, 4*pi)
    verificar(Imin, 4*pi)
    verificar(angulo, 0.0)
    Iu, Iv, Iuv = c2.inercias_eixos(
        xp=3,
        yp=4,
        angulo=45
    )
    verificar(Iu, 4*pi)
    verificar(Iv, 4*pi)
    verificar(Iuv, 0.0)
    Iu, Iv, Iuv = c2.inercias_eixos()
    verificar(Iu, 68*pi)
    verificar(Iv, 40*pi)
    verificar(Iuv, 48*pi)
    for r in [-2, 0]:
        try:
            Circulo(r=r)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Era esperado ValueError."
            )
    c3 = Circulo(r=2, sinal=-1)
    verificar(c3.area(), 4*pi)
    assert c3.sinal == -1

