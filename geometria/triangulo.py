
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
