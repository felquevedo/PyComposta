
from math import isclose

from .figura import Figura


class Poligono(Figura):
    """
    Polígono plano definido por vértices locais.

    Aceita polígonos convexos e côncavos,
    com vértices em sentido horário ou anti-horário.

    O contorno deve ser simples (sem cruzamentos).

    Parâmetros
    ----------
    vertices : sequência de pares (xi, eta)
        Vértices ordenados ao longo do contorno.
    x0, y0 : float
        Origem local no sistema global.
    theta : float
        Rotação anti-horária em graus.
    sinal : int
        +1 para área adicionada.
        -1 para área removida.
    """

    def __init__(
        self, vertices,
        x0=0.0, y0=0.0,
        theta=0.0, sinal=1
    ):
        super().__init__(x0, y0, theta, sinal)

        self.vertices = [
            tuple(map(float, p))
            for p in vertices
        ]

        # Aceita o primeiro vértice repetido no final.
        if (
            len(self.vertices) > 1
            and self.vertices[0] == self.vertices[-1]
        ):
            self.vertices.pop()

        if len(self.vertices) < 3:
            raise ValueError(
                "O polígono precisa de pelo menos "
                "três vértices."
            )

        # Validação geométrica usando Shapely.
        from shapely.geometry import Polygon

        geometria = Polygon(self.vertices)

        if not geometria.is_valid or geometria.is_empty:
            raise ValueError(
                "O polígono deve possuir um contorno "
                "simples, sem cruzamentos."
            )

        if geometria.area <= 1e-12:
            raise ValueError(
                "A área do polígono deve ser positiva."
            )

    def _integrar(self):
        """
        Calcula área, momentos estáticos e
        momentos de segunda ordem pela fórmula
        de Green, no sistema local.

        Retorna
        -------
        A, xc, yc, Ix0, Iy0, Ixy0
        """

        vertices = self.vertices
        n = len(vertices)

        soma_A = 0.0
        soma_x = 0.0
        soma_y = 0.0

        soma_Ix = 0.0
        soma_Iy = 0.0
        soma_Ixy = 0.0

        for i in range(n):

            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]

            delta = x1*y2 - x2*y1

            soma_A += delta

            soma_x += (x1+x2)*delta
            soma_y += (y1+y2)*delta

            soma_Ix += (
                y1**2 + y1*y2 + y2**2
            ) * delta

            soma_Iy += (
                x1**2 + x1*x2 + x2**2
            ) * delta

            soma_Ixy += (
                2*x1*y1
                + x1*y2
                + x2*y1
                + 2*x2*y2
            ) * delta

        As = soma_A / 2

        if abs(As) <= 1e-12:
            raise ValueError(
                "Área orientada nula."
            )

        orientacao = 1 if As > 0 else -1

        A = abs(As)

        xc = soma_x / (6*As)
        yc = soma_y / (6*As)

        Ix0 = orientacao*soma_Ix/12
        Iy0 = orientacao*soma_Iy/12
        Ixy0 = orientacao*soma_Ixy/24

        return A, xc, yc, Ix0, Iy0, Ixy0

    def area(self):
        A, *_ = self._integrar()
        return A

    def centroide_local(self):
        _, xc, yc, *_ = self._integrar()
        return xc, yc

    def inercias_centrais_locais(self):

        A, xc, yc, Ix0, Iy0, Ixy0 = (
            self._integrar()
        )

        Ix = Ix0 - A*yc**2
        Iy = Iy0 - A*xc**2
        Ixy = Ixy0 - A*xc*yc

        return Ix, Iy, Ixy


# ======================================================
# TESTES DO MÓDULO
# ======================================================

if __name__ == "__main__":

    from .retangulo import Retangulo
    from .triangulo import Triangulo

    def verificar(valor, esperado):
        assert isclose(
            valor, esperado,
            rel_tol=1e-9,
            abs_tol=1e-9
        ), f"Esperado {esperado}, obtido {valor}"

    # --------------------------------------------------
    # TESTE 1 - RETÂNGULO
    # --------------------------------------------------

    p1 = Poligono([
        (0, 0), (4, 0),
        (4, 2), (0, 2)
    ])

    verificar(p1.area(), 8)

    xc, yc = p1.centroide()

    verificar(xc, 2)
    verificar(yc, 1)

    Ix, Iy, Ixy = p1.inercias_centrais()

    verificar(Ix, 8/3)
    verificar(Iy, 32/3)
    verificar(Ixy, 0)

    print("Teste 1 - Retângulo: OK")

    # --------------------------------------------------
    # TESTE 2 - ORDEM DOS VÉRTICES
    # --------------------------------------------------

    p2 = Poligono(list(reversed(p1.vertices)))

    verificar(p2.area(), p1.area())

    for a, b in zip(
        p2.centroide(), p1.centroide()
    ):
        verificar(a, b)

    for a, b in zip(
        p2.inercias_centrais(),
        p1.inercias_centrais()
    ):
        verificar(a, b)

    print("Teste 2 - Ordem dos vértices: OK")

    # --------------------------------------------------
    # TESTE 3 - TRIÂNGULO
    # --------------------------------------------------

    p3 = Poligono([
        (0, 0), (4, 0), (0, 3)
    ])

    t3 = Triangulo(
        (0, 0), (4, 0), (0, 3)
    )

    verificar(p3.area(), t3.area())

    for a, b in zip(
        p3.centroide(), t3.centroide()
    ):
        verificar(a, b)

    for a, b in zip(
        p3.inercias_centrais(),
        t3.inercias_centrais()
    ):
        verificar(a, b)

    print("Teste 3 - Triângulo: OK")

    # --------------------------------------------------
    # TESTE 4 - POLÍGONO CÔNCAVO EM L
    # --------------------------------------------------

    p4 = Poligono([
        (0, 0), (4, 0), (4, 1),
        (1, 1), (1, 3), (0, 3)
    ])

    verificar(p4.area(), 6)

    xc, yc = p4.centroide()

    verificar(xc, 1.5)
    verificar(yc, 1.0)

    Ix, Iy, Ixy = p4.inercias_centrais()

    verificar(Ix, 4.0)
    verificar(Iy, 8.5)
    verificar(Ixy, -3.0)

    print("Teste 4 - Polígono côncavo: OK")

    # --------------------------------------------------
    # TESTE 5 - ROTAÇÃO E TRANSLAÇÃO
    # --------------------------------------------------

    p5 = Poligono(
        [(0, 0), (4, 0), (4, 2), (0, 2)],
        x0=3, y0=1, theta=30
    )

    r5 = Retangulo(
        b=4, h=2,
        x0=3, y0=1, theta=30
    )

    for a, b in zip(
        p5.centroide(), r5.centroide()
    ):
        verificar(a, b)

    for a, b in zip(
        p5.inercias_centrais(),
        r5.inercias_centrais()
    ):
        verificar(a, b)

    print("Teste 5 - Rotação e translação: OK")

    # --------------------------------------------------
    # TESTE 6 - MOMENTOS PRINCIPAIS
    # --------------------------------------------------

    xc, yc = p4.centroide()

    Imax, Imin, angulo = (
        p4.inercias_principais()
    )

    Iu, Iv, Iuv = p4.inercias_eixos(
        xp=xc, yp=yc, angulo=angulo
    )

    verificar(Iu, Imax)
    verificar(Iv, Imin)
    verificar(Iuv, 0)

    print("Teste 6 - Momentos principais: OK")

    # --------------------------------------------------
    # TESTE 7 - VALIDAÇÃO
    # --------------------------------------------------

    invalidos = [
        [(0, 0), (1, 1)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 0), (2, 2), (0, 2), (2, 0)]
    ]

    for vertices in invalidos:
        try:
            Poligono(vertices)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Era esperado ValueError."
            )

    vazado = Poligono(
        [(0, 0), (2, 0), (0, 2)],
        sinal=-1
    )

    verificar(vazado.area(), 2)
    assert vazado.sinal == -1

    print("Teste 7 - Validação: OK")

    print("\nTodos os testes de Poligono passaram!")
