
from math import pi, isclose
from .figura import Figura


class Circulo(Figura):
    """
    Círculo definido pelo raio r.

    A origem local está no centro do círculo.

    Parâmetros
    ----------
    r : float
        Raio do círculo.
    x0, y0 : float
        Coordenadas globais do centro.
    theta : float
        Rotação anti-horária, em graus.
    sinal : int
        +1 para área adicionada.
        -1 para área removida (vazado).
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
        return pi * self.r**2

    def centroide_local(self):
        """Retorna o centroide no sistema local."""
        return 0.0, 0.0

    def inercias_centrais_locais(self):
        """
        Retorna os momentos e o produto de inércia
        centroidais no sistema local.
        """

        I = pi * self.r**4 / 4

        return I, I, 0.0


# ======================================================
# TESTES DO MÓDULO
# ======================================================
