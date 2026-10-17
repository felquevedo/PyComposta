
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

if __name__ == "__main__":

    from math import isclose, pi

    from .retangulo import Retangulo
    from .circulo import Circulo
    from .semicirculo import Semicirculo
    from .triangulo import Triangulo

    def verificar(valor, esperado):
        assert isclose(
            valor, esperado,
            rel_tol=1e-8,
            abs_tol=1e-7
        ), f"Esperado {esperado}, obtido {valor}"

    # --------------------------------------------------
    # TESTE 1 - DOIS RETÂNGULOS JUSTAPOSTOS
    # --------------------------------------------------

    secao = SecaoComposta([
        Retangulo(b=2, h=4),
        Retangulo(b=2, h=4, x0=2)
    ])

    # Equivale a um retângulo de 4 x 4

    verificar(secao.area(), 16)

    xc, yc = secao.centroide()
    verificar(xc, 2)
    verificar(yc, 2)

    Ix, Iy, Ixy = secao.inercias_centrais()

    verificar(Ix, 4*4**3/12)
    verificar(Iy, 4*4**3/12)
    verificar(Ixy, 0)

    print("Teste 1 - Retângulos justapostos: OK")

    # --------------------------------------------------
    # TESTE 2 - RETÂNGULO COM FURO CENTRAL
    # --------------------------------------------------

    secao = SecaoComposta([
        Retangulo(b=10, h=6),
        Circulo(r=2, x0=5, y0=3, sinal=-1)
    ])

    verificar(secao.area(), 60-4*pi)

    xc, yc = secao.centroide()
    verificar(xc, 5)
    verificar(yc, 3)

    Ix, Iy, Ixy = secao.inercias_centrais()

    verificar(Ix, 10*6**3/12-4*pi)
    verificar(Iy, 6*10**3/12-4*pi)
    verificar(Ixy, 0)

    print("Teste 2 - Retângulo com furo: OK")

    # --------------------------------------------------
    # TESTE 3 - SEÇÃO DO EXEMPLO
    # --------------------------------------------------

    # Dimensões em mm:
    # largura = 120
    # altura do retângulo = 140
    # triângulo removido = 120 x 60
    # semicírculo externo: r = 60
    # furo circular: r = 40

    exemplo = SecaoComposta([
        Retangulo(
            b=120, h=140
        ),
        Triangulo(
            (0, 0), (120, 0), (120, 60),
            sinal=-1
        ),
        Semicirculo(
            r=60, x0=60, y0=140
        ),
        Circulo(
            r=40, x0=60, y0=140,
            sinal=-1
        )
    ])

    verificar(exemplo.area(), 13200+200*pi)

    xc, yc = exemplo.centroide()

    verificar(xc, 54.7932932091)
    verificar(yc, 96.6107767429)

    Ix, Iy, Ixy = exemplo.inercias_centrais()

    verificar(Ix, 34245226.846241)
    verificar(Iy, 18543877.911576)
    verificar(Ixy, 4795975.925487)

    print("Teste 3 - Seção do exemplo: OK")

    # --------------------------------------------------
    # TESTE 4 - EIXOS PRINCIPAIS
    # --------------------------------------------------

    Imax, Imin, angulo = (
        exemplo.inercias_principais()
    )

    verificar(Imax, 35594252.084327)
    verificar(Imin, 17194852.673491)
    verificar(angulo, 15.7103760472)

    Iu, Iv, Iuv = exemplo.inercias_eixos(
        xp=xc, yp=yc, angulo=angulo
    )

    verificar(Iu, Imax)
    verificar(Iv, Imin)
    verificar(Iuv, 0)

    print("Teste 4 - Eixos principais: OK")

    print(
        "\nTodos os testes de SecaoComposta passaram!"
    )
