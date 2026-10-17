
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

if __name__ == "__main__":

    def verificar(valor, esperado):
        assert isclose(
            valor, esperado,
            rel_tol=1e-9,
            abs_tol=1e-9
        ), f"Esperado {esperado}, obtido {valor}"

    # TESTE 1 - SEMICÍRCULO NA ORIGEM

    s1 = Semicirculo(r=2)

    verificar(s1.area(), 2*pi)

    xc, yc = s1.centroide()
    verificar(xc, 0.0)
    verificar(yc, 8/(3*pi))

    Ix, Iy, Ixy = s1.inercias_centrais()

    verificar(Ix, 16*(pi/8 - 8/(9*pi)))
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)

    print("Teste 1 - Propriedades locais: OK")

    # TESTE 2 - MOMENTOS NA ORIGEM

    Ix, Iy, Ixy = s1.inercias_origem()

    verificar(Ix, 2*pi)
    verificar(Iy, 2*pi)
    verificar(Ixy, 0.0)

    print("Teste 2 - Momentos na origem: OK")

    # TESTE 3 - TRANSLAÇÃO E ROTAÇÃO

    s2 = Semicirculo(
        r=2, x0=3, y0=1, theta=90
    )

    xc, yc = s2.centroide()

    verificar(xc, 3 - 8/(3*pi))
    verificar(yc, 1.0)

    Ix, Iy, Ixy = s2.inercias_centrais()

    verificar(Ix, 2*pi)
    verificar(Iy, 16*(pi/8 - 8/(9*pi)))
    verificar(Ixy, 0.0)

    print("Teste 3 - Rotação e translação: OK")

    # TESTE 4 - MOMENTOS PRINCIPAIS

    Imax, Imin, angulo = s1.inercias_principais()

    verificar(Imax, 2*pi)
    verificar(Imin, 16*(pi/8 - 8/(9*pi)))
    verificar(angulo, -90.0)

    print("Teste 4 - Momentos principais: OK")

    # TESTE 5 - VALIDAÇÃO

    for r in (-2, 0):
        try:
            Semicirculo(r)
        except ValueError:
            pass
        else:
            raise AssertionError("Era esperado ValueError.")

    vazado = Semicirculo(r=2, sinal=-1)
    verificar(vazado.area(), 2*pi)
    assert vazado.sinal == -1

    print("Teste 5 - Validação: OK")

    print("\nTodos os testes de Semicirculo passaram!")
