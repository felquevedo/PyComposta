
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

if __name__ == "__main__":

    def verificar(valor, esperado):
        assert isclose(
            valor, esperado,
            rel_tol=1e-9,
            abs_tol=1e-9
        ), f"Esperado {esperado}, obtido {valor}"

    # --------------------------------------------------
    # TESTE 1 - RETÂNGULO SEM ROTAÇÃO
    # --------------------------------------------------

    r1 = Retangulo(b=4, h=2)

    verificar(r1.area(), 8.0)

    xc, yc = r1.centroide()
    verificar(xc, 2.0)
    verificar(yc, 1.0)

    Ix, Iy, Ixy = r1.inercias_centrais()

    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0.0)

    # Momentos em relação à origem

    Ix, Iy, Ixy = r1.inercias_origem()

    verificar(Ix, 32/3)
    verificar(Iy, 128/3)
    verificar(Ixy, 16.0)

    print("Teste 1 - Sem rotação: OK")

    # --------------------------------------------------
    # TESTE 2 - ROTAÇÃO E TRANSLAÇÃO
    # --------------------------------------------------

    r2 = Retangulo(
        b=4,
        h=2,
        x0=3,
        y0=1,
        theta=30
    )

    verificar(r2.area(), 8.0)

    xc, yc = r2.centroide()

    verificar(xc, 4.232050807568877)
    verificar(yc, 2.8660254037844384)

    Ix, Iy, Ixy = r2.inercias_centrais()

    verificar(Ix, 4.666666666666667)
    verificar(Iy, 8.666666666666666)
    verificar(Ixy, -3.4641016151377544)

    print("Teste 2 - Rotação e translação: OK")

    # --------------------------------------------------
    # TESTE 3 - MOMENTOS PRINCIPAIS CENTRAIS
    # --------------------------------------------------

    Imax, Imin, angulo = r2.inercias_principais()

    verificar(Imax, 32/3)
    verificar(Imin, 8/3)
    verificar(angulo, -60.0)

    print("Teste 3 - Momentos principais: OK")

    # --------------------------------------------------
    # TESTE 4 - EIXOS ARBITRÁRIOS
    # --------------------------------------------------

    # Eixos passando pelo centroide e rotacionados
    # de 30 graus em relação ao sistema global.
    # Devem coincidir com os eixos locais da figura.

    Iu, Iv, Iuv = r2.inercias_eixos(
        xp=xc,
        yp=yc,
        angulo=30
    )

    verificar(Iu, 8/3)
    verificar(Iv, 32/3)
    verificar(Iuv, 0.0)

    # Eixos globais passando pela origem
    Iu, Iv, Iuv = r1.inercias_eixos()

    verificar(Iu, 32/3)
    verificar(Iv, 128/3)
    verificar(Iuv, 16.0)

    print("Teste 4 - Eixos arbitrários: OK")

    # --------------------------------------------------
    # TESTE 5 - VALIDAÇÃO DOS PARÂMETROS
    # --------------------------------------------------

    for b, h in [(-4, 2), (4, -2), (0, 2)]:
        try:
            Retangulo(b=b, h=h)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Era esperado ValueError."
            )

    # Verifica o sinal de um vazado
    r3 = Retangulo(b=4, h=2, sinal=-1)

    verificar(r3.area(), 8.0)
    assert r3.sinal == -1

    print("Teste 5 - Validação: OK")

    print("\nTodos os testes de Retangulo passaram!")
