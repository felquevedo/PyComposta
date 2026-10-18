
from math import atan2, cos, degrees, hypot, radians, sin

from .figura import Figura


class SecaoComposta:
    """
    Seção plana formada pela composição de figuras.

    Figuras com sinal=+1 adicionam área.
    Figuras com sinal=-1 removem área.

    Convenção:
        Ix  = integral(y**2 dA)
        Iy  = integral(x**2 dA)
        Ixy = integral(x*y dA)
    """

    def __init__(self, figuras=None):
        self.figuras = []

        if figuras is not None:
            for figura in figuras:
                self.adicionar(figura)

    def adicionar(self, figura):
        """Adiciona uma figura à seção."""

        if not isinstance(figura, Figura):
            raise TypeError(
                "O objeto deve ser uma instância de Figura."
            )

        self.figuras.append(figura)

    def remover(self, figura):
        """Remove uma figura da coleção."""
        self.figuras.remove(figura)

    def area(self):
        """Retorna a área resultante com sinais."""

        return sum(
            figura.sinal * figura.area()
            for figura in self.figuras
        )

    def _validar_area(self):
        """Verifica se a área resultante é positiva."""

        A = self.area()

        if A <= 0:
            raise ValueError(
                "A área resultante deve ser positiva."
            )

        return A

    def centroide(self):
        """Retorna o centroide global (xc, yc)."""

        A = self._validar_area()

        Sx = 0.0
        Sy = 0.0

        for figura in self.figuras:
            Ai = figura.sinal * figura.area()
            xi, yi = figura.centroide()

            Sx += Ai * xi
            Sy += Ai * yi

        return Sx / A, Sy / A

    def inercias_centrais(self):
        """
        Retorna (Ix, Iy, Ixy) em relação
        aos eixos centroidais globais.
        """

        xc, yc = self.centroide()

        Ix = 0.0
        Iy = 0.0
        Ixy = 0.0

        for figura in self.figuras:

            A = figura.area()
            s = figura.sinal

            xi, yi = figura.centroide()

            Ixi, Iyi, Ixyi = (
                figura.inercias_centrais()
            )

            dx = xi - xc
            dy = yi - yc

            Ix += s * (Ixi + A * dy**2)
            Iy += s * (Iyi + A * dx**2)
            Ixy += s * (Ixyi + A * dx * dy)

        return Ix, Iy, Ixy

    def inercias_origem(self):
        """
        Retorna (Ix, Iy, Ixy) em relação
        à origem global (0, 0).
        """

        self._validar_area()

        Ix = Iy = Ixy = 0.0

        for figura in self.figuras:
            Ixi, Iyi, Ixyi = figura.inercias_origem()
            s = figura.sinal

            Ix += s * Ixi
            Iy += s * Iyi
            Ixy += s * Ixyi

        return Ix, Iy, Ixy

    def inercias_eixos(
        self, xp=0.0, yp=0.0, angulo=0.0
    ):
        """
        Momentos em relação a eixos (u, v).

        Origem dos eixos: (xp, yp).
        Rotação anti-horária: angulo, em graus.
        """

        A = self._validar_area()
        xc, yc = self.centroide()

        Ix, Iy, Ixy = self.inercias_centrais()

        dx = xc - xp
        dy = yc - yp

        # Translação dos eixos
        Ix += A * dy**2
        Iy += A * dx**2
        Ixy += A * dx * dy

        # Rotação dos eixos
        t = radians(angulo)
        c = cos(t)
        s = sin(t)

        Iu = Ix*c**2 + Iy*s**2 + 2*Ixy*s*c
        Iv = Ix*s**2 + Iy*c**2 - 2*Ixy*s*c
        Iuv = (Iy-Ix)*s*c + Ixy*(c**2-s**2)

        return Iu, Iv, Iuv

    def inercias_principais(self, xp=None, yp=None):
        """
        Retorna (Imax, Imin, angulo_max).

        Sem xp, yp: eixos principais centroidais.
        Com xp, yp: eixos principais pelo ponto dado.
        """

        if xp is None and yp is None:
            Ix, Iy, Ixy = self.inercias_centrais()

        elif xp is not None and yp is not None:
            Ix, Iy, Ixy = self.inercias_eixos(
                xp=xp, yp=yp, angulo=0.0
            )

        else:
            raise ValueError(
                "Informe xp e yp juntos."
            )

        Im = (Ix + Iy) / 2
        R = hypot((Ix-Iy)/2, Ixy)

        Imax = Im + R
        Imin = Im - R

        if R <= 1e-12 * max(abs(Im), 1.0):
            angulo = 0.0
        else:
            angulo = degrees(
                0.5 * atan2(2*Ixy, Ix-Iy)
            )

            angulo = (angulo + 90) % 180 - 90

        return Imax, Imin, angulo


# ======================================================
# TESTES DO MÓDULO
# ======================================================
