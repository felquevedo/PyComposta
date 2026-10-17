
from math import isclose
from .figura import Figura


class Triangulo(Figura):
    """
    Triângulo definido por três vértices locais.

    Parâmetros
    ----------
    p1, p2, p3 : tuple
        Coordenadas (xi, eta) dos vértices.
    x0, y0 : float
        Coordenadas globais da origem local.
    theta : float
        Rotação anti-horária, em graus.
    sinal : int
        +1 para área adicionada.
        -1 para área removida.
    """

    def __init__(self, p1, p2, p3,
                 x0=0.0, y0=0.0,
                 theta=0.0, sinal=1):

        super().__init__(x0, y0, theta, sinal)

        self.p1 = tuple(map(float, p1))
        self.p2 = tuple(map(float, p2))
        self.p3 = tuple(map(float, p3))

        self.vertices = (self.p1, self.p2, self.p3)

        if self.area() <= 1e-12:
            raise ValueError(
                "Os vértices não podem ser colineares."
            )

    def area(self):
        """Área geométrica positiva."""

        (x1, y1), (x2, y2), (x3, y3) = self.vertices

        dobro_area = (
            x1*(y2-y3)
            + x2*(y3-y1)
            + x3*(y1-y2)
        )

        return abs(dobro_area)/2

    def centroide_local(self):
        """Centroide no sistema local."""

        xc = sum(p[0] for p in self.vertices)/3
        yc = sum(p[1] for p in self.vertices)/3

        return xc, yc

    def inercias_centrais_locais(self):
        """
        Momentos e produto de inércia centroidais.
        """

        A = self.area()
        xc, yc = self.centroide_local()

        u = [x-xc for x, y in self.vertices]
        v = [y-yc for x, y in self.vertices]

        Ix = A/12 * sum(vi**2 for vi in v)
        Iy = A/12 * sum(ui**2 for ui in u)
        Ixy = A/12 * sum(
            ui*vi for ui, vi in zip(u, v)
        )

        return Ix, Iy, Ixy


# ======================================================
# TESTES DO MÓDULO
# ======================================================

if __name__ == "__main__":

    def verificar(valor, esperado):
        assert isclose(
            valor, esperado,
            rel_tol=1e-9,
            abs_tol=1e-9
        ), f"Esperado {esperado}, obtido {valor}"

    # TESTE 1 - TRIÂNGULO RETÂNGULO

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

    print("Teste 1 - Triângulo retângulo: OK")

    # TESTE 2 - MOMENTOS NA ORIGEM

    Ix, Iy, Ixy = t1.inercias_origem()

    verificar(Ix, 9.0)
    verificar(Iy, 16.0)
    verificar(Ixy, 6.0)

    print("Teste 2 - Momentos na origem: OK")

    # TESTE 3 - ORDEM DOS VÉRTICES

    t2 = Triangulo(
        (0, 3), (4, 0), (0, 0)
    )

    verificar(t2.area(), t1.area())

    for a, b in zip(
        t2.inercias_centrais(),
        t1.inercias_centrais()
    ):
        verificar(a, b)

    print("Teste 3 - Ordem dos vértices: OK")

    # TESTE 4 - TRANSLAÇÃO E ROTAÇÃO

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

    print("Teste 4 - Rotação e translação: OK")

    # TESTE 5 - MOMENTOS PRINCIPAIS

    Imax, Imin, angulo = t1.inercias_principais()

    from math import sqrt, degrees, atan2

    Im = (3 + 16/3)/2
    R = sqrt(((3 - 16/3)/2)**2 + 4)

    verificar(Imax, Im + R)
    verificar(Imin, Im - R)

    # Confere que o produto de inércia se anula
    # quando os eixos são orientados pelo ângulo
    # principal retornado.

    xc, yc = t1.centroide()

    Iu, Iv, Iuv = t1.inercias_eixos(
        xp=xc, yp=yc, angulo=angulo
    )

    verificar(Iu, Imax)
    verificar(Iv, Imin)
    verificar(Iuv, 0.0)

    print("Teste 5 - Momentos principais: OK")

    # TESTE 6 - VALIDAÇÃO

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

    print("Teste 6 - Validação: OK")

    print("\nTodos os testes de Triangulo passaram!")
