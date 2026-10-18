
from math import isclose
from .figura import Figura


class Retangulo(Figura):
    """
    Retângulo definido pela base b e altura h.

    A origem local está no vértice inferior esquerdo.

    Parâmetros
    ----------
    b, h : float
        Base e altura do retângulo.
    x0, y0 : float
        Coordenadas globais da origem local.
    theta : float
        Rotação anti-horária, em graus.
    sinal : int
        +1 para área adicionada.
        -1 para área removida.
    """

    def __init__(self, b, h, x0=0.0, y0=0.0,
                 theta=0.0, sinal=1):

        super().__init__(x0, y0, theta, sinal)

        if b <= 0 or h <= 0:
            raise ValueError(
                "Base e altura devem ser positivas."
            )

        self.b = float(b)
        self.h = float(h)

    def area(self):
        """Retorna a área geométrica positiva."""

        return self.b * self.h

    def centroide_local(self):
        """Retorna o centroide no sistema local."""

        return self.b/2, self.h/2

    def inercias_centrais_locais(self):
        """
        Retorna os momentos e o produto de inércia
        centroidais no sistema local.
        """

        Ix = self.b * self.h**3 / 12
        Iy = self.h * self.b**3 / 12
        Ixy = 0.0

        return Ix, Iy, Ixy


# ======================================================
# TESTES DO MÓDULO
# ======================================================
