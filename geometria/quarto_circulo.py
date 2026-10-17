
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

if __name__ == "__main__":

    def verificar(valor, esperado):
        assert isclose(
            valor, esperado,
            rel_tol=1e-9,
            abs_tol=1e-9
        ), f"Esperado {esperado}, obtido {valor}"

    # --------------------------------------------------
    # TESTE 1 - PROPRIEDADES LOCAIS
    # --------------------------------------------------

    q1 = QuartoCirculo(r=2)

    verificar(q1.area(), pi)

    xc, yc = q1.centroide()

    verificar(xc, 8/(3*pi))
    verificar(yc, 8/(3*pi))

    Ix, Iy, Ixy = q1.inercias_centrais()

    verificar(Ix, 16*(pi/16 - 4/(9*pi)))
    verificar(Iy, 16*(pi/16 - 4/(9*pi)))
    verificar(Ixy, 16*(1/8 - 4/(9*pi)))

    print("Teste 1 - Propriedades locais: OK")

    # --------------------------------------------------
    # TESTE 2 - MOMENTOS NA ORIGEM
    # --------------------------------------------------

    Ix, Iy, Ixy = q1.inercias_origem()

    verificar(Ix, pi)
    verificar(Iy, pi)
    verificar(Ixy, 2.0)

    print("Teste 2 - Momentos na origem: OK")

    # --------------------------------------------------
    # TESTE 3 - ROTAÇÃO E TRANSLAÇÃO
    # --------------------------------------------------

    q2 = QuartoCirculo(
        r=2,
        x0=3,
        y0=1,
        theta=90
    )

    xc, yc = q2.centroide()

    verificar(xc, 3 - 8/(3*pi))
    verificar(yc, 1 + 8/(3*pi))

    Ix, Iy, Ixy = q2.inercias_centrais()

    Icentral = 16*(pi/16 - 4/(9*pi))
    Pcentral = 16*(1/8 - 4/(9*pi))

    verificar(Ix, Icentral)
    verificar(Iy, Icentral)
    verificar(Ixy, -Pcentral)

    print("Teste 3 - Rotação e translação: OK")

    # --------------------------------------------------
    # TESTE 4 - MOMENTOS PRINCIPAIS
    # --------------------------------------------------

    Imax, Imin, angulo = q1.inercias_principais()

    Icentral = 16*(pi/16 - 4/(9*pi))
    Pcentral = 16*(1/8 - 4/(9*pi))

    verificar(Imax, Icentral - Pcentral)
    verificar(Imin, Icentral + Pcentral)

    # O eixo de Imax está orientado a -45 graus.
    verificar(angulo, -45.0)

    print("Teste 4 - Momentos principais: OK")

    # --------------------------------------------------
    # TESTE 5 - EIXOS ARBITRÁRIOS
    # --------------------------------------------------

    # Eixos passando pelo centroide e rotacionados
    # de 45 graus em relação aos eixos globais.

    xc, yc = q1.centroide()

    Iu, Iv, Iuv = q1.inercias_eixos(
        xp=xc,
        yp=yc,
        angulo=45
    )

    verificar(Iu, Icentral + Pcentral)
    verificar(Iv, Icentral - Pcentral)
    verificar(Iuv, 0.0)


    print("Teste 5 - Eixos arbitrários: OK")

    # --------------------------------------------------
    # TESTE 6 - VALIDAÇÃO
    # --------------------------------------------------

    for r in (-2, 0):
        try:
            QuartoCirculo(r)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Era esperado ValueError."
            )

    vazado = QuartoCirculo(r=2, sinal=-1)

    verificar(vazado.area(), pi)
    assert vazado.sinal == -1

    print("Teste 6 - Validação: OK")

    print("\nTodos os testes de QuartoCirculo passaram!")
