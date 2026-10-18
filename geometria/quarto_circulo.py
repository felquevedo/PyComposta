
from math import pi, isclose
from .figura import Figura


class QuartoCirculo(Figura):
    """
    Quarto de círculo no primeiro quadrante.

    A origem local está no centro do círculo.

    Parâmetros
    ----------
    r : float
        Raio do círculo.
    x0, y0 : float
        Coordenadas globais da origem local.
    theta : float
        Rotação anti-horária, em graus.
    sinal : int
        +1 para área adicionada.
        -1 para área removida.
    """

    def __init__(self, r, x0=0.0, y0=0.0,
                 theta=0.0, sinal=1):

        super().__init__(x0, y0, theta, sinal)

        if r <= 0:
            raise ValueError(
                "O raio deve ser positivo."
            )

        self.r = float(r)

    def area(self):
        """Retorna a área geométrica positiva."""
        return pi * self.r**2 / 4

    def centroide_local(self):
        """Retorna o centroide no sistema local."""

        c = 4*self.r/(3*pi)
        return c, c

    def inercias_centrais_locais(self):
        """
        Retorna os momentos e o produto de inércia
        centroidais no sistema local.
        """

        r = self.r

        Ix = r**4 * (pi/16 - 4/(9*pi))
        Iy = r**4 * (pi/16 - 4/(9*pi))
        Ixy = r**4 * (1/8 - 4/(9*pi))

        return Ix, Iy, Ixy


# ======================================================
# TESTES DO MÓDULO
# ======================================================
