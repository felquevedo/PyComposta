# PyComposta

**PyComposta** é um aplicativo em Python para calcular e visualizar as propriedades geométricas de **seções planas compostas**, desenvolvido para uso didático nas disciplinas de Mecânica.

## Funcionalidades

- Composição de seções com retângulos, círculos, semicírculos, quartos de círculo, triângulos e polígonos, incluindo **vazios**.
- Cálculo de área, centroide, momentos e produto de inércia centroidais, momentos principais e orientação dos eixos principais.
- Visualização da seção, dos eixos e do **círculo de Mohr** (quando disponível na versão da interface).
- Inclusão e edição de figuras com **esquemas PNG** dos parâmetros; formulário compacto que permanece aberto ao adicionar figuras.
- Desenho de polígonos pelo mouse, zoom e ajuste à grade (*snap*).
- Abertura e salvamento de seções em **JSON**.

As unidades seguem as dimensões fornecidas: por exemplo, medidas em cm produzem áreas em cm² e momentos de inércia em cm⁴.

## Instalação e execução

Requer **Python 3.10+**, Tkinter e as dependências do projeto.

```bash
python -m pip install -r requirements.txt
python interface_pycomposta.py
```

O pacote **Pillow** é opcional e melhora o redimensionamento das imagens:

```bash
python -m pip install Pillow
```

Mantenha a pasta `figuras/` ao lado de `interface_pycomposta.py`, com os arquivos `retangulo.png`, `circulo.png`, `semicirculo.png`, `quartocirculo.png`, `triangulo.png` e `poligono.png`.

## Uso básico

Abra **Adicionar figura**, selecione a geometria, informe os parâmetros e clique em **Adicionar**. A janela permanece aberta para novos lançamentos; use **Fechar** ao terminar. Também é possível desenhar polígonos diretamente na área gráfica. Para representar furos, utilize figuras negativas. Salve ou abra suas seções pelo menu **Arquivo**.

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
