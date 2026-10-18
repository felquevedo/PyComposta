from geometria.secao_composta import SecaoComposta
from geometria.retangulo import Retangulo
from geometria.circulo import Circulo
from geometria.poligono import Poligono
from geometria.visualizacao import desenhar_secao
import matplotlib.pyplot as plt

# ---------------------------------------------------
# EX1: Retângulo de 20 x 30 com furo circular de raio
# ---------------------------------------------------

# Retângulo de 20 x 30 com furo circular de raio 5
secao = SecaoComposta()
secao.adicionar(Retangulo(b=20, h=30))
secao.adicionar(Circulo(r=5, x0=10, y0=15, sinal=-1))

A = secao.area()
xc, yc = secao.centroide()
Ix, Iy, Ixy = secao.inercias_centrais()
Imax, Imin, angulo = secao.inercias_principais()

print(f"Área: {A:.3f}")
print(f"Centroide: ({xc:.3f}, {yc:.3f})")
print(f"Ix = {Ix:.3f}; Iy = {Iy:.3f}; Ixy = {Ixy:.3f}")
print(f"Imax = {Imax:.3f}; Imin = {Imin:.3f}")
print(f"Ângulo principal: {angulo:.3f}°")

# ---------------------------------------------------
# EX2: Polígono com vértices
# ---------------------------------------------------

secao2 = SecaoComposta([
    Poligono([
        (0, 0),
        (120, 0),
        (120, 30),
        (30, 30),
        (30, 100),
        (0, 100)
    ])
])

print("Área:", secao2.area())
print("Centroide:", secao2.centroide())
print("Inércias:", secao2.inercias_centrais())
print("Principais:", secao2.inercias_principais())

# Representação geométrica do polígono
fig, ax = desenhar_secao(secao2)

# Círculo de Mohr dos momentos e produto de inércia centroidais
import math
from matplotlib.patches import Circle

Ix, Iy, Ixy = secao2.inercias_centrais()
Iu, Iv, theta = secao2.inercias_principais()
centro = (Ix + Iy) / 2
raio = math.hypot((Ix - Iy) / 2, Ixy)

fig_mohr, ax_mohr = plt.subplots()
ax_mohr.add_patch(Circle((centro, 0), raio, fill=False, lw=2))
ax_mohr.plot([Ix, Iy], [Ixy, -Ixy], "o--", label="Eixos x e y")
ax_mohr.plot([Iv, Iu], [0, 0], "o", label="Eixos principais")
ax_mohr.plot(centro, 0, "x", label="Centro")
ax_mohr.axhline(0, color="0.4", lw=0.8)
ax_mohr.set_aspect("equal", adjustable="box")
ax_mohr.set_xlabel("Momento de inércia, I")
ax_mohr.set_ylabel("Produto de inércia, Ixy")
ax_mohr.set_title("Círculo de Mohr — polígono")
ax_mohr.grid(True, linestyle=":", alpha=0.5)
ax_mohr.legend()
ax_mohr.relim()
ax_mohr.autoscale_view()
fig_mohr.tight_layout()

plt.show()