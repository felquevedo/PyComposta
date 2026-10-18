"""Testes de triangulo.

Cada teste documenta o objetivo do caso e compara valores numericos
com resultados de referencia usando a funcao verificar.
Os cenarios migrados mantem verificacoes acumuladas do codigo original.
"""
from geometria.triangulo import *
def verificar(valor, esperado):
    """Compara resultado e referencia com tolerancias numericas."""
    assert isclose(
        valor, esperado,
        rel_tol=1e-9,
        abs_tol=1e-9
    ), f"Esperado {esperado}, obtido {valor}"


def test_area_centroide_e_produto_de_inercia():
    """Verifica area centroide e produto de inercia.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    t1 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )
    verificar(t1.area(), 6.0)
    xc, yc = t1.centroide()
    verificar(xc, 4/3)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = t1.inercias_centrais()
    verificar(Ix, 3.0)
    verificar(Iy, 16/3)
    verificar(Ixy, -2.0)


def test_inercias_em_relacao_a_origem():
    """Verifica inercias em relacao a origem.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    t1 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )
    verificar(t1.area(), 6.0)
    xc, yc = t1.centroide()
    verificar(xc, 4/3)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = t1.inercias_centrais()
    verificar(Ix, 3.0)
    verificar(Iy, 16/3)
    verificar(Ixy, -2.0)
    Ix, Iy, Ixy = t1.inercias_origem()
    verificar(Ix, 9.0)
    verificar(Iy, 16.0)
    verificar(Ixy, 6.0)


def test_invariancia_a_ordem_dos_vertices():
    """Verifica invariancia a ordem dos vertices.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    t1 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )
    verificar(t1.area(), 6.0)
    xc, yc = t1.centroide()
    verificar(xc, 4/3)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = t1.inercias_centrais()
    verificar(Ix, 3.0)
    verificar(Iy, 16/3)
    verificar(Ixy, -2.0)
    Ix, Iy, Ixy = t1.inercias_origem()
    verificar(Ix, 9.0)
    verificar(Iy, 16.0)
    verificar(Ixy, 6.0)
    t2 = Triangulo(
        (0, 3), (4, 0), (0, 0)
    )
    verificar(t2.area(), t1.area())
    for a, b in zip(
        t2.inercias_centrais(),
        t1.inercias_centrais()
    ):
        verificar(a, b)


def test_translacao_e_rotacao_90_graus():
    """Verifica translacao e rotacao 90 graus.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    t1 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )
    verificar(t1.area(), 6.0)
    xc, yc = t1.centroide()
    verificar(xc, 4/3)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = t1.inercias_centrais()
    verificar(Ix, 3.0)
    verificar(Iy, 16/3)
    verificar(Ixy, -2.0)
    Ix, Iy, Ixy = t1.inercias_origem()
    verificar(Ix, 9.0)
    verificar(Iy, 16.0)
    verificar(Ixy, 6.0)
    t2 = Triangulo(
        (0, 3), (4, 0), (0, 0)
    )
    verificar(t2.area(), t1.area())
    for a, b in zip(
        t2.inercias_centrais(),
        t1.inercias_centrais()
    ):
        verificar(a, b)
    t3 = Triangulo(
        (0, 0), (4, 0), (0, 3),
        x0=5, y0=2, theta=90
    )
    xc, yc = t3.centroide()
    verificar(xc, 4.0)
    verificar(yc, 2 + 4/3)
    Ix, Iy, Ixy = t3.inercias_centrais()
    verificar(Ix, 16/3)
    verificar(Iy, 3.0)
    verificar(Ixy, 2.0)


def test_momentos_principais_e_eixos_rotacionados():
    """Verifica momentos principais e eixos rotacionados.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    t1 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )
    verificar(t1.area(), 6.0)
    xc, yc = t1.centroide()
    verificar(xc, 4/3)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = t1.inercias_centrais()
    verificar(Ix, 3.0)
    verificar(Iy, 16/3)
    verificar(Ixy, -2.0)
    Ix, Iy, Ixy = t1.inercias_origem()
    verificar(Ix, 9.0)
    verificar(Iy, 16.0)
    verificar(Ixy, 6.0)
    t2 = Triangulo(
        (0, 3), (4, 0), (0, 0)
    )
    verificar(t2.area(), t1.area())
    for a, b in zip(
        t2.inercias_centrais(),
        t1.inercias_centrais()
    ):
        verificar(a, b)
    t3 = Triangulo(
        (0, 0), (4, 0), (0, 3),
        x0=5, y0=2, theta=90
    )
    xc, yc = t3.centroide()
    verificar(xc, 4.0)
    verificar(yc, 2 + 4/3)
    Ix, Iy, Ixy = t3.inercias_centrais()
    verificar(Ix, 16/3)
    verificar(Iy, 3.0)
    verificar(Ixy, 2.0)
    Imax, Imin, angulo = t1.inercias_principais()
    from math import sqrt, degrees, atan2
    Im = (3 + 16/3)/2
    R = sqrt(((3 - 16/3)/2)**2 + 4)
    verificar(Imax, Im + R)
    verificar(Imin, Im - R)
    xc, yc = t1.centroide()
    Iu, Iv, Iuv = t1.inercias_eixos(
        xp=xc, yp=yc, angulo=angulo
    )
    verificar(Iu, Imax)
    verificar(Iv, Imin)
    verificar(Iuv, 0.0)


def test_vertices_invalidos_e_triangulo_vazado():
    """Verifica vertices invalidos e triangulo vazado.

    Este caso preserva as verificacoes acumuladas do teste original.
    """
    t1 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )
    verificar(t1.area(), 6.0)
    xc, yc = t1.centroide()
    verificar(xc, 4/3)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = t1.inercias_centrais()
    verificar(Ix, 3.0)
    verificar(Iy, 16/3)
    verificar(Ixy, -2.0)
    Ix, Iy, Ixy = t1.inercias_origem()
    verificar(Ix, 9.0)
    verificar(Iy, 16.0)
    verificar(Ixy, 6.0)
    t2 = Triangulo(
        (0, 3), (4, 0), (0, 0)
    )
    verificar(t2.area(), t1.area())
    for a, b in zip(
        t2.inercias_centrais(),
        t1.inercias_centrais()
    ):
        verificar(a, b)
    t3 = Triangulo(
        (0, 0), (4, 0), (0, 3),
        x0=5, y0=2, theta=90
    )
    xc, yc = t3.centroide()
    verificar(xc, 4.0)
    verificar(yc, 2 + 4/3)
    Ix, Iy, Ixy = t3.inercias_centrais()
    verificar(Ix, 16/3)
    verificar(Iy, 3.0)
    verificar(Ixy, 2.0)
    Imax, Imin, angulo = t1.inercias_principais()
    from math import sqrt, degrees, atan2
    Im = (3 + 16/3)/2
    R = sqrt(((3 - 16/3)/2)**2 + 4)
    verificar(Imax, Im + R)
    verificar(Imin, Im - R)
    xc, yc = t1.centroide()
    Iu, Iv, Iuv = t1.inercias_eixos(
        xp=xc, yp=yc, angulo=angulo
    )
    verificar(Iu, Imax)
    verificar(Iv, Imin)
    verificar(Iuv, 0.0)
    try:
        Triangulo(
            (0, 0), (1, 1), (2, 2)
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Era esperado ValueError."
        )
    vazado = Triangulo(
        (0, 0), (4, 0), (0, 3),
        sinal=-1
    )
    verificar(vazado.area(), 6.0)
    assert vazado.sinal == -1

