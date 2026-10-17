
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Polygon as MplPolygon
from matplotlib.patches import Arc
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.ops import unary_union

from geometria import figura

from .retangulo import Retangulo
from .circulo import Circulo
from .semicirculo import Semicirculo
from .quarto_circulo import QuartoCirculo
from .triangulo import Triangulo
from .secao_composta import SecaoComposta
from .poligono import Poligono


def pontos_figura(figura, n=360):
    """Retorna o contorno global de uma figura."""

    if isinstance(figura, Retangulo):
        pontos = [
            (0, 0),
            (figura.b, 0),
            (figura.b, figura.h),
            (0, figura.h)
        ]

    elif isinstance(figura, Circulo):
        t = np.linspace(0, 2*np.pi, n)
        pontos = [
            (figura.r*np.cos(a),
             figura.r*np.sin(a))
            for a in t
        ]

    elif isinstance(figura, Semicirculo):
        t = np.linspace(0, np.pi, n)
        pontos = [
            (figura.r*np.cos(a),
             figura.r*np.sin(a))
            for a in t
        ]

    elif isinstance(figura, QuartoCirculo):
        t = np.linspace(0, np.pi/2, n)
        pontos = [(0, 0)]
        pontos += [
            (figura.r*np.cos(a),
             figura.r*np.sin(a))
            for a in t
        ]

    elif isinstance(figura, Triangulo):
        pontos = list(figura.vertices)

    elif isinstance(figura, Poligono):
        pontos = list(figura.vertices)

    else:
        raise TypeError("Figura não suportada.")

    return np.array([
        figura.transformar_ponto(x, y)
        for x, y in pontos
    ])


def geometria_secao(secao, n=360):
    """
    Constrói a geometria resultante com Shapely.

    As figuras positivas são unidas.
    As negativas são subtraídas.
    """

    positivas = []
    negativas = []

    for figura in secao.figuras:
        pontos = pontos_figura(figura, n=n)
        poligono = ShapelyPolygon(pontos)

        if figura.sinal == 1:
            positivas.append(poligono)
        else:
            negativas.append(poligono)

    if not positivas:
        raise ValueError("A seção não possui áreas positivas.")

    geometria = unary_union(positivas)

    if negativas:
        vazios = unary_union(negativas)
        geometria = geometria.difference(vazios)

    return geometria


def desenhar_poligono(ax, poligono, cor="#A5C9E9"):
    """Desenha contorno externo e vazios."""

    exterior = np.array(poligono.exterior.coords)

    ax.fill(
        exterior[:, 0],
        exterior[:, 1],
        facecolor=cor,
        edgecolor="#27669A",
        linewidth=1.5
    )

    for interior in poligono.interiors:
        pontos = np.array(interior.coords)

        ax.fill(
            pontos[:, 0],
            pontos[:, 1],
            facecolor="white",
            edgecolor="#27669A",
            linewidth=1.5
        )


def desenhar_secao(
    secao,
    mostrar_componentes=False,
    mostrar_eixos=True,
    mostrar_centroide=True,
    mostrar_eixos_centrais=True,
    mostrar_eixos_principais=True,
    mostrar_propriedades=True
):
    """
    Desenha a seção composta e suas propriedades.
    """

    if not isinstance(secao, SecaoComposta):
        raise TypeError("Esperado SecaoComposta.")

    fig, ax = plt.subplots(figsize=(11, 8))

    geometria = geometria_secao(secao)

    # --------------------------------------------------
    # SEÇÃO FINAL
    # --------------------------------------------------

    if geometria.geom_type == "Polygon":
        desenhar_poligono(ax, geometria)

    elif geometria.geom_type == "MultiPolygon":
        for poligono in geometria.geoms:
            desenhar_poligono(ax, poligono)

    else:
        raise ValueError(
            "A geometria resultante não é poligonal."
        )

    # --------------------------------------------------
    # CONTORNOS DAS FIGURAS COMPONENTES
    # --------------------------------------------------

    if mostrar_componentes:
        for figura in secao.figuras:
            pontos = pontos_figura(figura)

            ax.plot(
                np.r_[pontos[:, 0], pontos[0, 0]],
                np.r_[pontos[:, 1], pontos[0, 1]],
                linestyle=":",
                linewidth=1,
                color="gray"
            )

    # --------------------------------------------------
    # LIMITES
    # --------------------------------------------------

    xmin, ymin, xmax, ymax = geometria.bounds

    escala = max(xmax-xmin, ymax-ymin, 1.0)
    margem = 0.15 * escala

    ax.set_xlim(xmin-margem, xmax+margem)
    ax.set_ylim(ymin-margem, ymax+margem)

    # --------------------------------------------------
    # EIXOS GLOBAIS
    # --------------------------------------------------

    if mostrar_eixos:
        ax.axhline(0, color="gray", linewidth=1)
        ax.axvline(0, color="gray", linewidth=1)

    # --------------------------------------------------
    # PROPRIEDADES
    # --------------------------------------------------

    A = secao.area()
    xc, yc = secao.centroide()
    Ix, Iy, Ixy = secao.inercias_centrais()

    Imax, Imin, angulo = (
        secao.inercias_principais()
    )

    # --------------------------------------------------
    # CENTROIDE
    # --------------------------------------------------

    if mostrar_centroide:
        ax.plot(
            xc, yc,
            marker="o",
            color="#B45309",
            markersize=6
        )

        ax.annotate(
            "C",
            (xc, yc),
            xytext=(7, 7),
            textcoords="offset points",
            fontsize=12,
            fontweight="bold"
        )

    # --------------------------------------------------
    # EIXOS CENTROIDAIS
    # --------------------------------------------------

    if mostrar_eixos_centrais:
        ax.axhline(
            yc,
            color="#D97706",
            linestyle="--",
            linewidth=1
        )

        ax.axvline(
            xc,
            color="#D97706",
            linestyle="--",
            linewidth=1
        )

    # --------------------------------------------------
    # EIXOS PRINCIPAIS
    # --------------------------------------------------

    if mostrar_eixos_principais:

        t = np.radians(angulo)
        comprimento = 0.45 * escala

        dx = comprimento*np.cos(t)
        dy = comprimento*np.sin(t)

        ax.plot(
            [xc-dx, xc+dx],
            [yc-dy, yc+dy],
            color="#16836D",
            linewidth=1.8
        )

        ax.plot(
            [xc+dy, xc-dy],
            [yc-dx, yc+dx],
            color="#8B5CF6",
            linewidth=1.8
        )

        ax.text(
            xc+dx, yc+dy, "u",
            color="#16836D",
            fontsize=12,
            fontweight="bold"
        )

        ax.text(
            xc-dy, yc+dx, "v",
            color="#8B5CF6",
            fontsize=12,
            fontweight="bold"
        )

        # Arco representando o ângulo principal
        raio_arco = 0.16 * escala

        inicio = min(0, angulo)
        fim = max(0, angulo)

        arco = Arc(
            (xc, yc),
            2*raio_arco,
            2*raio_arco,
            theta1=inicio,
            theta2=fim,
            color="#16836D",
            linewidth=1.3
        )

        ax.add_patch(arco)

        ax.text(
            xc+raio_arco,
            yc+0.04*escala,
            rf"$\theta_p={angulo:.2f}^\circ$",
            fontsize=10
        )

    # --------------------------------------------------
    # QUADRO DE PROPRIEDADES
    # --------------------------------------------------

    if mostrar_propriedades:

        texto = (
            f"Área = {A:.3f}\n"
            f"xc = {xc:.3f}\n"
            f"yc = {yc:.3f}\n"
            f"Ix = {Ix:.3f}\n"
            f"Iy = {Iy:.3f}\n"
            f"Ixy = {Ixy:.3f}\n"
            f"Imax = {Imax:.3f}\n"
            f"Imin = {Imin:.3f}\n"
            f"Ângulo = {angulo:.3f}°"
        )

        fig.text(
            0.73, 0.50,
            texto,
            fontsize=10,
            va="center",
            family="monospace",
            bbox=dict(
                boxstyle="round",
                facecolor="#F5F5F5",
                edgecolor="#BBBBBB"
            )
        )

        fig.subplots_adjust(right=0.70)

    # --------------------------------------------------
    # FORMATAÇÃO
    # --------------------------------------------------

    ax.set_aspect("equal", adjustable="box")

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.set_title("PyComposta - Propriedades geométricas")

    ax.grid(True, linestyle=":", alpha=0.3)

    return fig, ax


# ======================================================
# TESTE DO MÓDULO
# ======================================================

if __name__ == "__main__":

    exemplo = SecaoComposta([
        Retangulo(b=120, h=140),

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

    fig, ax = desenhar_secao(
        exemplo,
        mostrar_componentes=False,
        mostrar_propriedades=True
    )

    plt.show()
