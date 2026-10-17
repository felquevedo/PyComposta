
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

if __name__ == "__main__":

    def verificar(valor, esperado):
        assert isclose(
            valor, esperado,
            rel_tol=1e-9,
            abs_tol=1e-9
        ), f"Esperado {esperado}, obtido {valor}"

    # --------------------------------------------------
    # TESTE 1 - CÍRCULO NA ORIGEM
    # --------------------------------------------------

    c1 = Circulo(r=2)

    verificar(c1.area(), 4*pi)

    xc, yc = c1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 0.0)

    Ix, Iy, Ixy = c1.inercias_centrais()

    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)

    print("Teste 1 - Círculo na origem: OK")

    # --------------------------------------------------
    # TESTE 2 - TRANSLAÇÃO E ROTAÇÃO
    # --------------------------------------------------

    c2 = Circulo(
        r=2,
        x0=3,
        y0=4,
        theta=30
    )

    verificar(c2.area(), 4*pi)

    xc, yc = c2.centroide()

    verificar(xc, 3.0)
    verificar(yc, 4.0)

    Ix, Iy, Ixy = c2.inercias_centrais()

    verificar(Ix, 4*pi)
    verificar(Iy, 4*pi)
    verificar(Ixy, 0.0)

    print("Teste 2 - Translação e rotação: OK")

    # --------------------------------------------------
    # TESTE 3 - MOMENTOS EM RELAÇÃO À ORIGEM
    # --------------------------------------------------

    Ix, Iy, Ixy = c2.inercias_origem()

    verificar(Ix, 68*pi)
    verificar(Iy, 40*pi)
    verificar(Ixy, 48*pi)

    print("Teste 3 - Inércias na origem: OK")

    # --------------------------------------------------
    # TESTE 4 - MOMENTOS PRINCIPAIS
    # --------------------------------------------------

    Imax, Imin, angulo = c2.inercias_principais()

    verificar(Imax, 4*pi)
    verificar(Imin, 4*pi)

    # Qualquer orientação é principal.
    # Por convenção, retorna 0 graus.
    verificar(angulo, 0.0)

    print("Teste 4 - Momentos principais: OK")

    # --------------------------------------------------
    # TESTE 5 - EIXOS ARBITRÁRIOS
    # --------------------------------------------------

    # Eixos passando pelo centroide, rotacionados
    # de 45 graus em relação aos globais.

    Iu, Iv, Iuv = c2.inercias_eixos(
        xp=3,
        yp=4,
        angulo=45
    )

    verificar(Iu, 4*pi)
    verificar(Iv, 4*pi)
    verificar(Iuv, 0.0)

    # Eixos globais passando pela origem
    Iu, Iv, Iuv = c2.inercias_eixos()

    verificar(Iu, 68*pi)
    verificar(Iv, 40*pi)
    verificar(Iuv, 48*pi)

    print("Teste 5 - Eixos arbitrários: OK")

    # --------------------------------------------------
    # TESTE 6 - VALIDAÇÃO DOS PARÂMETROS
    # --------------------------------------------------

    for r in [-2, 0]:
        try:
            Circulo(r=r)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Era esperado ValueError."
            )

    # Círculo utilizado como vazado
    c3 = Circulo(r=2, sinal=-1)

    verificar(c3.area(), 4*pi)
    assert c3.sinal == -1

    print("Teste 6 - Validação: OK")

    print("\nTodos os testes de Circulo passaram!")
