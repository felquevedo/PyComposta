"""Casos originais de retangulo, migrados de __main__ sem alterar as asserções."""
from geometria.retangulo import *
def verificar(valor, esperado):
    assert isclose(
        valor, esperado,
        rel_tol=1e-9,
        abs_tol=1e-9
    ), f"Esperado {esperado}, obtido {valor}"


def test_original_01():
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


def test_original_02():
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


def test_original_03():
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


def test_original_04():
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


def test_original_05():
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

