
from math import pi, isclose
from .figura import Figura


class Semicirculo(Figura):
    """
    Semicírculo superior de raio r.

    Origem local: centro do diâmetro.
    Região local: eta >= 0.
    """

    def __init__(self, r, x0=0.0, y0=0.0,
                 theta=0.0, sinal=1):

        super().__init__(x0, y0, theta, sinal)

        if r <= 0:
            raise ValueError("O raio deve ser positivo.")

        self.r = float(r)

    def area(self):
        return pi * self.r**2 / 2

    def centroide_local(self):
        return 0.0, 4*self.r/(3*pi)

    def inercias_centrais_locais(self):

        r = self.r

        Ix = r**4 * (pi/8 - 8/(9*pi))
        Iy = pi*r**4/8
        Ixy = 0.0

        return Ix, Iy, Ixy


# ======================================================
# TESTES DO MÓDULO
# ======================================================
