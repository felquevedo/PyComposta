
from abc import ABC, abstractmethod
from math import cos, sin, radians, sqrt, atan2, degrees, hypot


class Figura(ABC):
    """
    Classe abstrata para figuras geométricas planas.

    Convenções
    ----------
    x0, y0 : float
        Coordenadas globais da origem local.
    theta : float
        Rotação anti-horária, em graus.
    sinal : int
        +1 para área adicionada.
        -1 para área removida (vazado).

    Momentos de inércia:
        Ix  = integral(y² dA)
        Iy  = integral(x² dA)
        Ixy = integral(x*y dA)

    Os métodos geométricos retornam propriedades
    positivas da figura. O sinal será considerado
    pela classe SecaoComposta.
    """

    def __init__(self, x0=0.0, y0=0.0,
                 theta=0.0, sinal=1):

        if sinal not in (-1, 1):
            raise ValueError("O sinal deve ser +1 ou -1.")

        self.x0 = float(x0)
        self.y0 = float(y0)
        self.theta = float(theta)
        self.sinal = sinal

    # ==================================================
    # MÉTODOS ABSTRATOS
    # ==================================================

    @abstractmethod
    def area(self):
        """Retorna a área geométrica positiva."""
        pass

    @abstractmethod
    def centroide_local(self):
        """Retorna (xi_c, eta_c)."""
        pass

    @abstractmethod
    def inercias_centrais_locais(self):
        """Retorna (Ix, Iy, Ixy) centroidais locais."""
        pass

    # ==================================================
    # TRANSFORMAÇÕES GEOMÉTRICAS
    # ==================================================

    def transformar_ponto(self, xi, eta):
        """Transforma coordenadas locais em globais."""

        t = radians(self.theta)
        c, s = cos(t), sin(t)

        x = self.x0 + xi*c - eta*s
        y = self.y0 + xi*s + eta*c

        return x, y

    def centroide(self):
        """Retorna o centroide em coordenadas globais."""

        xi, eta = self.centroide_local()

        return self.transformar_ponto(xi, eta)

    # ==================================================
    # MOMENTOS CENTRAIS GLOBAIS
    # ==================================================

    def inercias_centrais(self):
        """
        Retorna os momentos e o produto de inércia
        centroidais nos eixos paralelos aos globais.

        Retorno
        -------
        Ix, Iy, Ixy : float
        """

        Ix, Iy, Ixy = self.inercias_centrais_locais()

        t = radians(self.theta)
        c, s = cos(t), sin(t)

        Ix_g = Ix*c*c + Iy*s*s - 2*Ixy*s*c
        Iy_g = Ix*s*s + Iy*c*c + 2*Ixy*s*c
        Ixy_g = (Ix-Iy)*s*c + Ixy*(c*c-s*s)

        return Ix_g, Iy_g, Ixy_g

    # ==================================================
    # MOMENTOS EM RELAÇÃO À ORIGEM GLOBAL
    # ==================================================

    def inercias_origem(self):
        """
        Retorna os momentos e o produto de inércia
        em relação à origem global (0,0).
        """

        A = self.area()
        xc, yc = self.centroide()

        Ix_c, Iy_c, Ixy_c = self.inercias_centrais()

        Ix = Ix_c + A*yc**2
        Iy = Iy_c + A*xc**2
        Ixy = Ixy_c + A*xc*yc

        return Ix, Iy, Ixy

    # ==================================================
    # MOMENTOS EM RELAÇÃO A EIXOS ARBITRÁRIOS
    # ==================================================

    def inercias_eixos(self, xp=0.0, yp=0.0,
                      angulo=0.0):
        """
        Retorna (Iu, Iv, Iuv) em relação aos eixos
        (u,v) que passam pelo ponto (xp,yp).

        O ângulo é medido do eixo x para o eixo u,
        positivo no sentido anti-horário.
        """

        A = self.area()
        xc, yc = self.centroide()

        Ix_c, Iy_c, Ixy_c = self.inercias_centrais()

        dx = xc - xp
        dy = yc - yp

        # Translação dos eixos
        Ix = Ix_c + A*dy**2
        Iy = Iy_c + A*dx**2
        Ixy = Ixy_c + A*dx*dy

        # Rotação dos eixos
        t = radians(angulo)
        c, s = cos(t), sin(t)


        Iu = Ix*c*c + Iy*s*s + 2*Ixy*s*c
        Iv = Ix*s*s + Iy*c*c - 2*Ixy*s*c
        Iuv = (Iy-Ix)*s*c + Ixy*(c*c-s*s)


        return Iu, Iv, Iuv

    # ==================================================
    # MOMENTOS PRINCIPAIS
    # ==================================================


    def inercias_principais(self, xp=None, yp=None):
        """
        Retorna (Imax, Imin, angulo_max).

        Por padrão, utiliza os eixos centroidais.

        angulo_max:
            Orientação do eixo de maior momento
            de inércia, em graus, no intervalo
            [-90, 90).
        """

        if xp is None and yp is None:
            Ix, Iy, Ixy = self.inercias_centrais()

        elif xp is not None and yp is not None:
            Ix, Iy, Ixy = self.inercias_eixos(
                xp=xp, yp=yp, angulo=0.0
            )

        else:
            raise ValueError(
                "Informe xp e yp simultaneamente."
            )

        Im = (Ix + Iy) / 2
        R = hypot((Ix - Iy) / 2, Ixy)

        Imax = Im + R
        Imin = Im - R

        if R <= 1e-12 * max(abs(Im), 1.0):
            angulo_max = 0.0
        else:
            angulo_max = degrees(
                0.5 * atan2(2*Ixy, Ix-Iy)
            )

            # Normaliza para [-90, 90)
            angulo_max = (
                (angulo_max + 90.0) % 180.0
            ) - 90.0

        return Imax, Imin, angulo_max

