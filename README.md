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
- Visualização opcional do **círculo de Mohr** dos momentos de inércia, com identificação do centro, raio, momentos principais e ângulo, nas versões da interface que oferecem esse recurso.

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
│   ├── dados/                  # Seis seções de referência em JSON
│   ├── conftest.py
│   ├── test_figuras.py
│   ├── test_retangulo.py
│   ├── test_circulo.py
│   ├── test_semicirculo.py
│   ├── test_quarto_circulo.py
│   ├── test_triangulo.py
│   ├── test_poligono.py
│   ├── test_secao_composta.py
│   └── test_exemplos_json.py
├── .github/workflows/testes.yml
├── interface_pycomposta.py
├── logo_ufrgs.png
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── LEIA-ME-TESTES.md
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
python -m pip install -r requirements.txt
```

Inicie a interface:

```bash
python interface_pycomposta.py
```

> O endereço do `git clone` é ilustrativo: substitua `SEU-USUARIO` pelo proprietário real do repositório. Confira também o nome real do arquivo de entrada da interface: algumas versões foram distribuídas com nomes diferentes de `interface_pycomposta.py`.

## Utilização básica

1. Clique em **Adicionar figura** para inserir uma figura geométrica, ou clique diretamente no gráfico para começar a desenhar um polígono.
2. No desenho por mouse, clique para marcar os vértices. Clique próximo ao primeiro vértice para fechar o polígono; também é possível concluir com **Enter** ou botão direito, ou cancelar com **Esc**.
3. Use a opção **Polígono negativo** para representar vazios e **Snap na grade** para alinhar os pontos à malha.
4. Marque as opções de visualização para exibir os eixos e as propriedades desejadas.
5. Utilize **Arquivo → Salvar** para guardar a seção em `.json` e **Arquivo → Abrir** para recuperá-la.

## Testes

Os testes automatizados são executados com **pytest**. Os casos que antes estavam nos blocos `if __name__ == "__main__"` dos módulos geométricos foram migrados para arquivos individuais na pasta `testes/`, com nomes descritivos e comentários explicativos. Dessa forma, os módulos de cálculo não precisam executar testes quando são importados.

Instale as dependências de desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

Execute a suíte completa, com relatório detalhado:

```bash
python -m pytest -v
```

Também é possível executar um conjunto específico:

```bash
python -m pytest testes/test_triangulo.py -v
python -m pytest testes/test_exemplos_json.py -v
```

**Cobertura atual:** propriedades geométricas de figuras isoladas, composição de seções, validações de entrada e seis exemplos de regressão armazenados em `testes/dados/`. A migração e revisão anteriores resultaram em **55 testes aprovados** no ambiente em que a suíte foi preparada; essa quantidade não substitui a execução na sua instalação.

**Precisão:** alguns resultados de referência dos exemplos JSON foram disponibilizados com arredondamento, portanto os testes correspondentes utilizam tolerâncias compatíveis. Consulte `LEIA-ME-TESTES.md` para detalhes.

**Limitações:** a suíte ainda não verifica automaticamente as interações gráficas do Tkinter nem a representação visual do círculo de Mohr.

### Integração contínua

O arquivo `.github/workflows/testes.yml` configura a execução dos testes no **GitHub Actions** em eventos de `push` e `pull request`, nas versões de Python especificadas no workflow.

### Arquivos que não devem ser versionados

Pastas como `__pycache__/` e `.pytest_cache/`, além de arquivos `*.pyc`, são temporários. Devem constar do `.gitignore`. Se já tiverem sido rastreados pelo Git, é necessário removê-los do índice sem apagar os arquivos locais.

## Autoria

**Felipe Pinto da Motta Quevedo**  
Universidade Federal do Rio Grande do Sul (UFRGS)

O projeto tem finalidade acadêmica e educacional. A menção à UFRGS identifica a vinculação institucional do autor e não implica endosso institucional ao software.

## Licença

Distribuído sob a **Licença MIT**. Consulte o arquivo [LICENSE](LICENSE).

O código é disponibilizado **sem garantias**. Resultados empregados em projetos profissionais devem ser verificados independentemente.

O logotipo da UFRGS é um elemento de identidade institucional e **não está coberto pela licença MIT do código-fonte**; seu uso deve respeitar as regras aplicáveis à marca.
