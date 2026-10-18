# PyComposta

**PyComposta** é um aplicativo em Python para calcular e visualizar as propriedades geométricas de **seções planas compostas**, desenvolvido para uso didático em Mecânica.

## Funcionalidades da interface

- Composição de seções com retângulos, círculos, semicírculos, quartos de círculo, triângulos e polígonos, incluindo **vazios**.
- Cálculo de área, centroide, momentos e produto de inércia centroidais, momentos principais e orientação dos eixos principais.
- Visualização da seção, dos eixos e do **círculo de Mohr** (quando disponível na versão da interface).
- Desenho de polígonos pelo mouse, zoom e ajuste à grade (*snap*).
- Abertura e salvamento de seções em **JSON**.

As unidades seguem as dimensões fornecidas: por exemplo, medidas em cm produzem áreas em cm² e momentos de inércia em cm⁴.

## Baixar e instalar no Windows

Para utilizar o **PyComposta sem instalar Python**, baixe o instalador na página de versões do projeto:

**[Baixar PyComposta para Windows (GitHub Releases)](https://github.com/felquevedo/PyComposta/releases/latest)**

1. Acesse o link acima.
2. Na versão mais recente, expanda a seção **Assets**, se necessário.
3. Clique no arquivo `PyComposta_Setup_1.0.0.exe` (ou no instalador da versão mais recente) para fazer o download.
4. Abra o arquivo `.exe` baixado e siga as instruções do assistente de instalação.
5. Inicie o **PyComposta** pelo menu Iniciar ou pelo atalho na área de trabalho, caso tenha optado por criá-lo.

O instalador inclui as dependências necessárias: **não é preciso instalar Python, Matplotlib ou outras bibliotecas separadamente**. O link acima funcionará quando a primeira versão estiver publicada no GitHub Releases do repositório `felquevedo/PyComposta`.

## Instalação a partir do código-fonte (desenvolvedores)

Requer **Python 3.10+**, Tkinter e as dependências do projeto.

Crie e ative um ambiente virtual na raiz do projeto:

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Com o ambiente ativado, instale as dependências e execute a interface:

```bash
python -m pip install -r requirements.txt
python interface_pycomposta.py
```

Para sair do ambiente virtual, execute `deactivate`.

O **Pillow** é utilizado para melhorar o redimensionamento das imagens e está listado em `requirements.txt`.

Mantenha a pasta `figuras/` ao lado de `interface_pycomposta.py`, com os arquivos `retangulo.png`, `circulo.png`, `semicirculo.png`, `quartocirculo.png`, `triangulo.png` e `poligono.png`.

## Uso básico

Abra **Adicionar figura**, selecione a geometria, informe os parâmetros e clique em **Adicionar**. A janela permanece aberta para novos lançamentos; use **Fechar** ao terminar. Também é possível desenhar polígonos diretamente na área gráfica. Para representar furos, utilize figuras negativas. Salve ou abra suas seções pelo menu **Arquivo**.

## Uso dos módulos em scripts Python

Além da interface gráfica, é possível importar as classes de `geometria/` em outros scripts. Por exemplo, crie um arquivo `main.py` na raiz do projeto:

```python
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
```

Execute com `python main.py`. No segundo exemplo, são exibidos a seção poligonal e o círculo de Mohr, com os pontos `(Ix, Ixy)`, `(Iy, -Ixy)` e os momentos principais `Iu` e `Iv`. O argumento `sinal=-1` representa um vazio. As unidades são determinadas pelas dimensões de entrada.

## Testes automatizados

Os testes com **pytest** estão na pasta `testes/`, incluindo verificações por figura e seis exemplos de regressão em JSON.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

O projeto inclui execução automatizada pelo **GitHub Actions**. Mais informações estão em `LEIA-ME-TESTES.md`.

## Autoria e licença

**Felipe Pinto da Motta Quevedo** — Universidade Federal do Rio Grande do Sul (UFRGS).

Projeto de finalidade acadêmica e educacional, distribuído sob a **licença MIT** (consulte `LICENSE`). A afiliação institucional não implica endosso da universidade ao software. O logotipo da UFRGS não está coberto pela licença do código. Resultados para uso profissional devem ser verificados independentemente.
