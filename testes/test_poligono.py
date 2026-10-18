"""Casos originais de poligono, migrados de __main__ sem alterar as asserções."""
from geometria.poligono import *
from geometria.retangulo import Retangulo
from geometria.triangulo import Triangulo
def verificar(valor, esperado):
    assert isclose(
        valor, esperado,
        rel_tol=1e-9,
        abs_tol=1e-9
    ), f"Esperado {esperado}, obtido {valor}"


def test_original_01():
    p1 = Poligono([
        (0, 0), (4, 0),
        (4, 2), (0, 2)
    ])
    verificar(p1.area(), 8)
    xc, yc = p1.centroide()
    verificar(xc, 2)
    verificar(yc, 1)
    Ix, Iy, Ixy = p1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0)


def test_original_02():
    p1 = Poligono([
        (0, 0), (4, 0),
        (4, 2), (0, 2)
    ])
    verificar(p1.area(), 8)
    xc, yc = p1.centroide()
    verificar(xc, 2)
    verificar(yc, 1)
    Ix, Iy, Ixy = p1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0)
    p2 = Poligono(list(reversed(p1.vertices)))
    verificar(p2.area(), p1.area())
    for a, b in zip(
        p2.centroide(), p1.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p2.inercias_centrais(),
        p1.inercias_centrais()
    ):
        verificar(a, b)


def test_original_03():
    p1 = Poligono([
        (0, 0), (4, 0),
        (4, 2), (0, 2)
    ])
    verificar(p1.area(), 8)
    xc, yc = p1.centroide()
    verificar(xc, 2)
    verificar(yc, 1)
    Ix, Iy, Ixy = p1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0)
    p2 = Poligono(list(reversed(p1.vertices)))
    verificar(p2.area(), p1.area())
    for a, b in zip(
        p2.centroide(), p1.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p2.inercias_centrais(),
        p1.inercias_centrais()
    ):
        verificar(a, b)
    p3 = Poligono([
        (0, 0), (4, 0), (0, 3)
    ])
    t3 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )
    verificar(p3.area(), t3.area())
    for a, b in zip(
        p3.centroide(), t3.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p3.inercias_centrais(),
        t3.inercias_centrais()
    ):
        verificar(a, b)


def test_original_04():
    p1 = Poligono([
        (0, 0), (4, 0),
        (4, 2), (0, 2)
    ])
    verificar(p1.area(), 8)
    xc, yc = p1.centroide()
    verificar(xc, 2)
    verificar(yc, 1)
    Ix, Iy, Ixy = p1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0)
    p2 = Poligono(list(reversed(p1.vertices)))
    verificar(p2.area(), p1.area())
    for a, b in zip(
        p2.centroide(), p1.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p2.inercias_centrais(),
        p1.inercias_centrais()
    ):
        verificar(a, b)
    p3 = Poligono([
        (0, 0), (4, 0), (0, 3)
    ])
    t3 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )
    verificar(p3.area(), t3.area())
    for a, b in zip(
        p3.centroide(), t3.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p3.inercias_centrais(),
        t3.inercias_centrais()
    ):
        verificar(a, b)
    p4 = Poligono([
        (0, 0), (4, 0), (4, 1),
        (1, 1), (1, 3), (0, 3)
    ])
    verificar(p4.area(), 6)
    xc, yc = p4.centroide()
    verificar(xc, 1.5)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = p4.inercias_centrais()
    verificar(Ix, 4.0)
    verificar(Iy, 8.5)
    verificar(Ixy, -3.0)


def test_original_05():
    p1 = Poligono([
        (0, 0), (4, 0),
        (4, 2), (0, 2)
    ])
    verificar(p1.area(), 8)
    xc, yc = p1.centroide()
    verificar(xc, 2)
    verificar(yc, 1)
    Ix, Iy, Ixy = p1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0)
    p2 = Poligono(list(reversed(p1.vertices)))
    verificar(p2.area(), p1.area())
    for a, b in zip(
        p2.centroide(), p1.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p2.inercias_centrais(),
        p1.inercias_centrais()
    ):
        verificar(a, b)
    p3 = Poligono([
        (0, 0), (4, 0), (0, 3)
    ])
    t3 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )
    verificar(p3.area(), t3.area())
    for a, b in zip(
        p3.centroide(), t3.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p3.inercias_centrais(),
        t3.inercias_centrais()
    ):
        verificar(a, b)
    p4 = Poligono([
        (0, 0), (4, 0), (4, 1),
        (1, 1), (1, 3), (0, 3)
    ])
    verificar(p4.area(), 6)
    xc, yc = p4.centroide()
    verificar(xc, 1.5)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = p4.inercias_centrais()
    verificar(Ix, 4.0)
    verificar(Iy, 8.5)
    verificar(Ixy, -3.0)
    p5 = Poligono(
        [(0, 0), (4, 0), (4, 2), (0, 2)],
        x0=3, y0=1, theta=30
    )
    r5 = Retangulo(
        b=4, h=2,
        x0=3, y0=1, theta=30
    )
    for a, b in zip(
        p5.centroide(), r5.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p5.inercias_centrais(),
        r5.inercias_centrais()
    ):
        verificar(a, b)


def test_original_06():
    p1 = Poligono([
        (0, 0), (4, 0),
        (4, 2), (0, 2)
    ])
    verificar(p1.area(), 8)
    xc, yc = p1.centroide()
    verificar(xc, 2)
    verificar(yc, 1)
    Ix, Iy, Ixy = p1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0)
    p2 = Poligono(list(reversed(p1.vertices)))
    verificar(p2.area(), p1.area())
    for a, b in zip(
        p2.centroide(), p1.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p2.inercias_centrais(),
        p1.inercias_centrais()
    ):
        verificar(a, b)
    p3 = Poligono([
        (0, 0), (4, 0), (0, 3)
    ])
    t3 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )
    verificar(p3.area(), t3.area())
    for a, b in zip(
        p3.centroide(), t3.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p3.inercias_centrais(),
        t3.inercias_centrais()
    ):
        verificar(a, b)
    p4 = Poligono([
        (0, 0), (4, 0), (4, 1),
        (1, 1), (1, 3), (0, 3)
    ])
    verificar(p4.area(), 6)
    xc, yc = p4.centroide()
    verificar(xc, 1.5)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = p4.inercias_centrais()
    verificar(Ix, 4.0)
    verificar(Iy, 8.5)
    verificar(Ixy, -3.0)
    p5 = Poligono(
        [(0, 0), (4, 0), (4, 2), (0, 2)],
        x0=3, y0=1, theta=30
    )
    r5 = Retangulo(
        b=4, h=2,
        x0=3, y0=1, theta=30
    )
    for a, b in zip(
        p5.centroide(), r5.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p5.inercias_centrais(),
        r5.inercias_centrais()
    ):
        verificar(a, b)
    xc, yc = p4.centroide()
    Imax, Imin, angulo = (
        p4.inercias_principais()
    )
    Iu, Iv, Iuv = p4.inercias_eixos(
        xp=xc, yp=yc, angulo=angulo
    )
    verificar(Iu, Imax)
    verificar(Iv, Imin)
    verificar(Iuv, 0)


def test_original_07():
    p1 = Poligono([
        (0, 0), (4, 0),
        (4, 2), (0, 2)
    ])
    verificar(p1.area(), 8)
    xc, yc = p1.centroide()
    verificar(xc, 2)
    verificar(yc, 1)
    Ix, Iy, Ixy = p1.inercias_centrais()
    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0)
    p2 = Poligono(list(reversed(p1.vertices)))
    verificar(p2.area(), p1.area())
    for a, b in zip(
        p2.centroide(), p1.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p2.inercias_centrais(),
        p1.inercias_centrais()
    ):
        verificar(a, b)
    p3 = Poligono([
        (0, 0), (4, 0), (0, 3)
    ])
    t3 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )
    verificar(p3.area(), t3.area())
    for a, b in zip(
        p3.centroide(), t3.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p3.inercias_centrais(),
        t3.inercias_centrais()
    ):
        verificar(a, b)
    p4 = Poligono([
        (0, 0), (4, 0), (4, 1),
        (1, 1), (1, 3), (0, 3)
    ])
    verificar(p4.area(), 6)
    xc, yc = p4.centroide()
    verificar(xc, 1.5)
    verificar(yc, 1.0)
    Ix, Iy, Ixy = p4.inercias_centrais()
    verificar(Ix, 4.0)
    verificar(Iy, 8.5)
    verificar(Ixy, -3.0)
    p5 = Poligono(
        [(0, 0), (4, 0), (4, 2), (0, 2)],
        x0=3, y0=1, theta=30
    )
    r5 = Retangulo(
        b=4, h=2,
        x0=3, y0=1, theta=30
    )
    for a, b in zip(
        p5.centroide(), r5.centroide()
    ):
        verificar(a, b)
    for a, b in zip(
        p5.inercias_centrais(),
        r5.inercias_centrais()
    ):
        verificar(a, b)
    xc, yc = p4.centroide()
    Imax, Imin, angulo = (
        p4.inercias_principais()
    )
    Iu, Iv, Iuv = p4.inercias_eixos(
        xp=xc, yp=yc, angulo=angulo
    )
    verificar(Iu, Imax)
    verificar(Iv, Imin)
    verificar(Iuv, 0)
    invalidos = [
        [(0, 0), (1, 1)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 0), (2, 2), (0, 2), (2, 0)]
    ]
    for vertices in invalidos:
        try:
            Poligono(vertices)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Era esperado ValueError."
            )
    vazado = Poligono(
        [(0, 0), (2, 0), (0, 2)],
        sinal=-1
    )
    verificar(vazado.area(), 2)
    assert vazado.sinal == -1

