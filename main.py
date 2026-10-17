from geometria.poligono import Poligono
from geometria.secao_composta import SecaoComposta
from geometria.visualizacao import desenhar_secao

import matplotlib.pyplot as plt

secao = SecaoComposta([
    Poligono([
        (0, 0),
        (120, 0),
        (120, 30),
        (30, 30),
        (30, 100),
        (0, 100)
    ])
])

print("Área:", secao.area())
print("Centroide:", secao.centroide())
print("Inércias:", secao.inercias_centrais())
print("Principais:", secao.inercias_principais())

fig, ax = desenhar_secao(secao)
plt.show()