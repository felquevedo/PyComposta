"""Casos originais de semicirculo, migrados de __main__ sem alterar as asserções."""
from geometria.semicirculo import *
def verificar(valor, esperado):
    assert isclose(
        valor, esperado,
        rel_tol=1e-9,
        abs_tol=1e-9
    ), f"Esperado {esperado}, obtido {valor}"


def test_original_01():
    s1 = Semicirculo(r=2)
    verificar(s1.area(), 2*pi)
    xc, yc = s1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 8/(3*pi))
    Ix, Iy, Ixy = s1.inercias_centrais()
    verificar(Ix, 16*(pi/8 - 8/(9*pi)))
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)


def test_original_02():
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


def test_original_03():
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


def test_original_04():
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


def test_original_05():
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

