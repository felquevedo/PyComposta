# PyComposta

**PyComposta** é um aplicativo em Python para a determinação e visualização das **propriedades geométricas de seções planas compostas**, desenvolvido com foco em aplicações didáticas de Mecânica e Engenharia Civil.

O programa permite combinar figuras planas, incluindo vazios, e visualizar os eixos de referência e as propriedades geométricas resultantes.

## Funcionalidades

- Composição de seções com **retângulos, círculos, semicírculos, quartos de círculo, triângulos e polígonos**.
- Adição, edição e exclusão de figuras; representação de áreas **positivas e negativas** (vazios).
- Cálculo de **área**, **centroide**, **momentos de inércia centroidais**, **produto de inércia** e **momentos principais de inércia** (`Iu` e `Iv`).
- Visualização dos **eixos globais**, **eixos centroidais**, **eixos principais** e das propriedades **por partes**.
- Desenho de polígonos diretamente no gráfico, com opção de ajuste à grade (*snap*), tolerância para fechamento e controles pelo mouse/teclado.
- Zoom no gráfico e comando **Exibir todos os objetos**.
- Abertura e salvamento de seções no formato **JSON**.

> **Unidades:** o programa trabalha com unidades consistentes com as dimensões informadas pelo usuário. Por exemplo, entradas em cm produzem área em cm² e momentos de inércia em cm⁴.

## Estrutura do projeto

```text
PyComposta/
├── geometria/
│   ├── circulo.py
│   ├── figura.py
│   ├── poligono.py
│   ├── quarto_circulo.py
│   ├── retangulo.py
│   ├── secao_composta.py
│   ├── semicirculo.py
│   ├── triangulo.py
│   └── visualizacao.py
├── testes/
├── interface_pycomposta.py
├── logo_ufrgs.png
├── main.py
├── .gitignore
├── LICENSE
└── README.md
```

## Requisitos

- Python 3.10 ou superior (recomendado).
- `matplotlib`.
- `tkinter` (normalmente incluído nas instalações do Python para Windows; em algumas distribuições Linux precisa ser instalado separadamente).
- Eventuais dependências adicionais utilizadas pelos módulos de `geometria/`.

## Instalação e execução

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/SEU-USUARIO/PyComposta.git
cd PyComposta
```

Opcionalmente, crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

Instale a biblioteca de visualização:

```bash
python -m pip install matplotlib
```

Inicie a interface:

```bash
python interface_pycomposta.py
```

> O endereço do `git clone` é ilustrativo: substitua `SEU-USUARIO` pelo proprietário real do repositório. Antes da primeira publicação, confira se os módulos geométricos exigem outras bibliotecas e acrescente-as aos requisitos.

## Utilização básica

1. Clique em **Adicionar figura** para inserir uma figura geométrica, ou clique diretamente no gráfico para começar a desenhar um polígono.
2. No desenho por mouse, clique para marcar os vértices. Clique próximo ao primeiro vértice para fechar o polígono; também é possível concluir com **Enter** ou botão direito, ou cancelar com **Esc**.
3. Use a opção **Polígono negativo** para representar vazios e **Snap na grade** para alinhar os pontos à malha.
4. Marque as opções de visualização para exibir os eixos e as propriedades desejadas.
5. Utilize **Arquivo → Salvar** para guardar a seção em `.json` e **Arquivo → Abrir** para recuperá-la.

## Testes

O diretório `testes/` é destinado às verificações do programa. Execute os testes conforme os scripts disponíveis nesse diretório.

## Autoria

**Felipe Pinto da Motta Quevedo**  
Universidade Federal do Rio Grande do Sul (UFRGS)

O projeto tem finalidade acadêmica e educacional. A menção à UFRGS identifica a vinculação institucional do autor e não implica endosso institucional ao software.

## Licença

Distribuído sob a **Licença MIT**. Consulte o arquivo [LICENSE](LICENSE).

O código é disponibilizado **sem garantias**. Resultados empregados em projetos profissionais devem ser verificados independentemente.

O logotipo da UFRGS é um elemento de identidade institucional e **não está coberto pela licença MIT do código-fonte**; seu uso deve respeitar as regras aplicáveis à marca.
