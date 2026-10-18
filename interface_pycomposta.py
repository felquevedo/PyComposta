
import tkinter as tk
import copy
import math
import json
from pathlib import Path
from types import SimpleNamespace
from tkinter import ttk, messagebox, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.patches import PathPatch

from geometria.retangulo import Retangulo
from geometria.circulo import Circulo
from geometria.semicirculo import Semicirculo
from geometria.quarto_circulo import QuartoCirculo
from geometria.triangulo import Triangulo
from geometria.poligono import Poligono
from geometria.secao_composta import SecaoComposta
from geometria.visualizacao import desenhar_secao


class FormularioFigura(tk.Toplevel):
    """
    Formulário para adicionar ou editar figuras.

    resultado:
        Figura criada, ou None se cancelado.
    """

    TIPOS = (
        "Retangulo",
        "Circulo",
        "Semicirculo",
        "QuartoCirculo",
        "Triangulo",
        "Poligono"
    )

    def __init__(self, master, figura=None):
        super().__init__(master)

        self.title(
            "Editar figura" if figura else "Adicionar figura"
        )
        self.geometry("460x570")
        self.resizable(False, False)

        self.resultado = None
        self.figura_original = figura

        self.transient(master)
        self.grab_set()

        self.tipo = tk.StringVar()
        self.sinal = tk.StringVar(value="+1")

        self.campos = {}

        self.criar_formulario()

        if figura is not None:
            self.preencher(figura)
        else:
            self.tipo.set("Retangulo")
            self.atualizar_campos()

        self.protocol(
            "WM_DELETE_WINDOW", self.destroy
        )

    def criar_formulario(self):

        frm = ttk.Frame(self, padding=15)
        frm.pack(fill="both", expand=True)

        ttk.Label(
            frm, text="Tipo de figura:"
        ).pack(anchor="w")

        cmb_tipo = ttk.Combobox(
            frm,
            textvariable=self.tipo,
            values=self.TIPOS,
            state="readonly"
        )
        cmb_tipo.pack(fill="x", pady=(3, 12))

        cmb_tipo.bind(
            "<<ComboboxSelected>>",
            lambda e: self.atualizar_campos()
        )

        self.frm_parametros = ttk.LabelFrame(
            frm,
            text="Parâmetros geométricos",
            padding=10
        )
        self.frm_parametros.pack(
            fill="both", expand=True
        )

        frm_botoes = ttk.Frame(frm)
        frm_botoes.pack(
            fill="x", pady=(15, 0)
        )

        ttk.Button(
            frm_botoes,
            text="Cancelar",
            command=self.destroy
        ).pack(side="right", padx=5)

        ttk.Button(
            frm_botoes,
            text="Confirmar",
            command=self.confirmar
        ).pack(side="right", padx=5)

    def criar_campo(self, nome, valor="0"):

        ttk.Label(
            self.frm_parametros,
            text=nome
        ).pack(anchor="w")

        entrada = ttk.Entry(
            self.frm_parametros
        )
        entrada.insert(0, str(valor))
        entrada.pack(
            fill="x", pady=(0, 8)
        )

        self.campos[nome] = entrada

    def atualizar_campos(self):

        for widget in self.frm_parametros.winfo_children():
            widget.destroy()

        self.campos = {}

        tipo = self.tipo.get()

        if tipo == "Retangulo":
            self.criar_campo("b", "100")
            self.criar_campo("h", "100")

        elif tipo in (
            "Circulo",
            "Semicirculo",
            "QuartoCirculo"
        ):
            self.criar_campo("r", "50")

        elif tipo == "Triangulo":
            self.criar_campo(
                "vertices",
                "0,0; 100,0; 0,100"
            )

        elif tipo == "Poligono":
            self.criar_campo(
                "vertices",
                "0,0; 100,0; 100,100; 0,100"
            )

        self.criar_campo("x0", "0")
        self.criar_campo("y0", "0")
        self.criar_campo("theta", "0")

        ttk.Label(
            self.frm_parametros,
            text="Operação:"
        ).pack(anchor="w")

        ttk.Radiobutton(
            self.frm_parametros,
            text="Adicionar área (+)",
            variable=self.sinal,
            value="+1"
        ).pack(anchor="w")

        ttk.Radiobutton(
            self.frm_parametros,
            text="Remover área (-)",
            variable=self.sinal,
            value="-1"
        ).pack(anchor="w")

    def obter_valor(self, nome):
        return float(
            self.campos[nome].get().strip()
            .replace(",", ".")
        )

    def obter_vertices(self):

        texto = self.campos[
            "vertices"
        ].get()

        vertices = []

        for ponto in texto.split(";"):
            valores = ponto.strip().split(",")

            if len(valores) != 2:
                raise ValueError(
                    "Use o formato x,y; x,y; x,y."
                )

            x, y = map(float, valores)
            vertices.append((x, y))

        return vertices

    def confirmar(self):

        try:
            tipo = self.tipo.get()

            parametros = dict(
                x0=self.obter_valor("x0"),
                y0=self.obter_valor("y0"),
                theta=self.obter_valor("theta"),
                sinal=int(self.sinal.get())
            )

            if tipo == "Retangulo":
                figura = Retangulo(
                    b=self.obter_valor("b"),
                    h=self.obter_valor("h"),
                    **parametros
                )

            elif tipo == "Circulo":
                figura = Circulo(
                    r=self.obter_valor("r"),
                    **parametros
                )

            elif tipo == "Semicirculo":
                figura = Semicirculo(
                    r=self.obter_valor("r"),
                    **parametros
                )

            elif tipo == "QuartoCirculo":
                figura = QuartoCirculo(
                    r=self.obter_valor("r"),
                    **parametros
                )

            elif tipo == "Triangulo":
                vertices = self.obter_vertices()

                if len(vertices) != 3:
                    raise ValueError(
                        "O triângulo exige três vértices."
                    )

                figura = Triangulo(
                    *vertices,
                    **parametros
                )

            elif tipo == "Poligono":
                figura = Poligono(
                    self.obter_vertices(),
                    **parametros
                )

            else:
                raise ValueError(
                    "Tipo de figura inválido."
                )

            self.resultado = figura
            self.destroy()

        except (ValueError, TypeError, KeyError) as erro:
            messagebox.showerror(
                "Dados inválidos",
                str(erro),
                parent=self
            )

    def preencher(self, figura):

        tipo = type(figura).__name__

        self.tipo.set(tipo)
        self.atualizar_campos()

        valores = {
            "x0": figura.x0,
            "y0": figura.y0,
            "theta": figura.theta
        }

        if isinstance(figura, Retangulo):
            valores.update(
                b=figura.b,
                h=figura.h
            )

        elif isinstance(
            figura,
            (Circulo, Semicirculo, QuartoCirculo)
        ):
            valores["r"] = figura.r

        elif isinstance(figura, Triangulo):
            valores["vertices"] = "; ".join(
                f"{x},{y}"
                for x, y in figura.vertices
            )

        elif isinstance(figura, Poligono):
            valores["vertices"] = "; ".join(
                f"{x},{y}"
                for x, y in figura.vertices
            )

        for nome, valor in valores.items():
            campo = self.campos[nome]
            campo.delete(0, tk.END)
            campo.insert(0, str(valor))

        self.sinal.set(str(figura.sinal))


class InterfacePyComposta(tk.Tk):
    """
    Interface principal do PyComposta.

    Primeira versão:
    - Lista de figuras
    - Visualização da seção
    - Propriedades geométricas
    - Carregamento de exemplo
    """

    def __init__(self):
        super().__init__()

        self.title("PyComposta - Propriedades Geométricas")
        self.geometry("1250x780")
        self.minsize(1000, 650)

        self.secao = SecaoComposta()
        self.figura_mpl = None
        self.canvas_mpl = None
        self._resize_job = None
        self._contornos_selecao = []
        self.modo_poligono = False
        self.vertices_desenho = []
        self.artistas_desenho = []
        self.sinal_poligono = 1
        self.snap_ativo = tk.BooleanVar(value=True)
        self.poligono_negativo = tk.BooleanVar(value=False)
        self.bind("<Escape>", lambda _event: self.cancelar_poligono_mouse()
                  if self.modo_poligono else None)

        # Controles de visualização.
        self.mostrar_eixos = tk.BooleanVar(value=True)
        self.mostrar_centroide = tk.BooleanVar(value=True)
        self.mostrar_por_partes = tk.BooleanVar(value=False)
        self.mostrar_eixos_centrais = tk.BooleanVar(value=True)
        self.mostrar_eixos_principais = tk.BooleanVar(value=True)
        self.mostrar_mohr = tk.BooleanVar(value=False)
        self.janela_mohr = None
        self.figura_mohr = None
        self.canvas_mohr = None
        self.espacamento_x = tk.StringVar(value="20")
        self.espacamento_y = tk.StringVar(value="20")

        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        self.criar_interface()
        self.criar_menu()
        self.carregar_exemplo()

    def criar_menu(self):
        """Menu principal para persistência de seções e informações do aplicativo."""
        barra = tk.Menu(self)
        arquivo = tk.Menu(barra, tearoff=False)
        arquivo.add_command(label="Abrir...", command=self.abrir_arquivo, accelerator="Ctrl+O")
        arquivo.add_command(label="Salvar...", command=self.salvar_arquivo, accelerator="Ctrl+S")
        arquivo.add_separator()
        arquivo.add_command(label="Fechar", command=self.fechar_aplicacao, accelerator="Alt+F4")
        barra.add_cascade(label="Arquivo", menu=arquivo)
        barra.add_command(label="Sobre", command=self.mostrar_sobre)
        self.config(menu=barra)
        self.bind_all("<Control-o>", lambda e: self.abrir_arquivo())
        self.bind_all("<Control-s>", lambda e: self.salvar_arquivo())

    @staticmethod
    def _serializar_figura(figura):
        tipo = type(figura).__name__
        dados = {"tipo": tipo, "x0": float(figura.x0), "y0": float(figura.y0),
                 "theta": float(figura.theta), "sinal": int(figura.sinal)}
        if tipo == "Retangulo":
            dados.update(b=float(figura.b), h=float(figura.h))
        elif tipo in ("Circulo", "Semicirculo", "QuartoCirculo"):
            dados["r"] = float(figura.r)
        elif tipo in ("Triangulo", "Poligono"):
            dados["vertices"] = [[float(x), float(y)] for x, y in figura.vertices]
        else:
            raise ValueError(f"Tipo de figura não suportado: {tipo}")
        return dados

    @staticmethod
    def _desserializar_figura(dados):
        if not isinstance(dados, dict):
            raise ValueError("Dados de figura inválidos.")
        tipo = dados["tipo"]
        parametros = {chave: float(dados[chave]) for chave in ("x0", "y0", "theta")}
        parametros["sinal"] = int(dados["sinal"])
        if parametros["sinal"] not in (-1, 1):
            raise ValueError("O sinal da figura deve ser +1 ou -1.")
        if tipo == "Retangulo":
            return Retangulo(b=float(dados["b"]), h=float(dados["h"]), **parametros)
        if tipo in ("Circulo", "Semicirculo", "QuartoCirculo"):
            classe = {"Circulo": Circulo, "Semicirculo": Semicirculo,
                      "QuartoCirculo": QuartoCirculo}[tipo]
            return classe(r=float(dados["r"]), **parametros)
        if tipo in ("Triangulo", "Poligono"):
            vertices = [(float(x), float(y)) for x, y in dados["vertices"]]
            if tipo == "Triangulo":
                if len(vertices) != 3:
                    raise ValueError("Triângulo deve conter três vértices.")
                return Triangulo(*vertices, **parametros)
            return Poligono(vertices, **parametros)
        raise ValueError(f"Tipo de figura desconhecido: {tipo}")

    def salvar_arquivo(self):
        caminho = filedialog.asksaveasfilename(
            parent=self, title="Salvar seção", defaultextension=".json",
            filetypes=[("Seção PyComposta (*.json)", "*.json"), ("Todos os arquivos", "*.*")],
        )
        if not caminho:
            return
        try:
            dados = {
                "formato": "PyComposta", "versao_formato": 1,
                "figuras": [self._serializar_figura(f) for f in self.secao.figuras],
                "visualizacao": {
                    "eixos_globais": self.mostrar_eixos.get(),
                    "centroide": self.mostrar_centroide.get(),
                    "eixos_centroidais": self.mostrar_eixos_centrais.get(),
                    "eixos_principais": self.mostrar_eixos_principais.get(),
                    "por_partes": self.mostrar_por_partes.get(),
                    "circulo_mohr": self.mostrar_mohr.get(),
                    "snap": self.snap_ativo.get(),
                    "poligono_negativo": self.poligono_negativo.get(),
                    "espacamento_x": self.espacamento_x.get(),
                    "espacamento_y": self.espacamento_y.get(),
                },
            }
            Path(caminho).write_text(json.dumps(dados, indent=2, ensure_ascii=False), encoding="utf-8")
        except (OSError, TypeError, ValueError) as erro:
            messagebox.showerror("Erro ao salvar", str(erro), parent=self)

    def abrir_arquivo(self):
        caminho = filedialog.askopenfilename(
            parent=self, title="Abrir seção",
            filetypes=[("Seção PyComposta (*.json)", "*.json"), ("Todos os arquivos", "*.*")],
        )
        if not caminho:
            return
        try:
            dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
            if not isinstance(dados, dict) or dados.get("formato") != "PyComposta":
                raise ValueError("O arquivo não contém uma seção PyComposta válida.")
            if dados.get("versao_formato") != 1:
                raise ValueError("Versão do formato de arquivo não suportada.")
            figuras = [self._desserializar_figura(item) for item in dados["figuras"]]
            nova_secao = SecaoComposta(figuras)
            if figuras:
                # Validação antecipada, antes de substituir o projeto aberto.
                nova_secao.area()
                nova_secao.centroide()
            visual = dados.get("visualizacao", {})
            if not isinstance(visual, dict):
                raise ValueError("Configuração de visualização inválida.")
            for chave in ("espacamento_x", "espacamento_y"):
                passo = float(str(visual.get(chave, "20")).replace(",", "."))
                if not math.isfinite(passo) or passo <= 0:
                    raise ValueError(f"Espaçamento inválido: {chave}")
        except (OSError, ValueError, TypeError, KeyError, IndexError) as erro:
            messagebox.showerror("Erro ao abrir", str(erro), parent=self)
            return
        self.cancelar_poligono_mouse()
        self.secao = nova_secao
        self.lst_figuras.selection_clear(0, tk.END)
        opcoes = {
            "eixos_globais": self.mostrar_eixos,
            "centroide": self.mostrar_centroide,
            "eixos_centroidais": self.mostrar_eixos_centrais,
            "eixos_principais": self.mostrar_eixos_principais,
            "por_partes": self.mostrar_por_partes,
            "circulo_mohr": self.mostrar_mohr,
            "snap": self.snap_ativo,
            "poligono_negativo": self.poligono_negativo,
            "espacamento_x": self.espacamento_x,
            "espacamento_y": self.espacamento_y,
        }
        for chave, variavel in opcoes.items():
            if chave in visual:
                variavel.set(visual[chave])
        self.atualizar_interface()

    def mostrar_sobre(self):
        janela = tk.Toplevel(self)
        janela.title("Sobre o PyComposta")
        janela.resizable(False, False)
        janela.transient(self)
        janela.grab_set()
        painel = ttk.Frame(janela, padding=24)
        painel.pack(fill="both", expand=True)
        # Reserva espaço para o logotipo institucional. Se existir um arquivo
        # logo_ufrgs.png junto ao script, ele é exibido automaticamente.
        area_logo = ttk.Frame(painel, width=220, height=105, relief="groove", borderwidth=1)
        area_logo.pack(pady=(0, 14))
        area_logo.pack_propagate(False)
        caminho_logo = Path(__file__).resolve().parent / "logo_ufrgs.png"
        try:
            if not caminho_logo.is_file():
                raise FileNotFoundError
            imagem_logo = tk.PhotoImage(file=str(caminho_logo))
            # Reduz imagens grandes, sem dependências adicionais.
            fator = max(1, math.ceil(max(imagem_logo.width() / 200,
                                          imagem_logo.height() / 90)))
            if fator > 1:
                imagem_logo = imagem_logo.subsample(fator, fator)
            rotulo_logo = ttk.Label(area_logo, image=imagem_logo)
            rotulo_logo.image = imagem_logo  # mantém referência à imagem
            rotulo_logo.place(relx=0.5, rely=0.5, anchor="center")
        except (FileNotFoundError, tk.TclError):
            ttk.Label(area_logo, text="Espaço para o logotipo da UFRGS",
                      foreground="gray", anchor="center", justify="center",
                      wraplength=190).place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(painel, text="PyComposta", font=("Segoe UI", 18, "bold")).pack(pady=(0, 6))
        ttk.Label(painel, text="Propriedades geométricas de seções compostas",
                  font=("Segoe UI", 10)).pack(pady=(0, 14))
        ttk.Separator(painel, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(painel, text="Desenvolvimento: Felipe Quevedo", justify="center").pack(pady=3)
        ttk.Label(painel, text="Universidade Federal do Rio Grande do Sul (UFRGS)",
                  justify="center").pack(pady=3)
        ttk.Label(painel, text="Aplicativo para estudo e cálculo de propriedades\n"
                  "geométricas de seções planas compostas.", justify="center").pack(pady=12)
        ttk.Label(painel, text="Uso acadêmico e educacional. Verifique os resultados\n"
                  "antes de utilizá-los em aplicações profissionais.", justify="center",
                  foreground="gray").pack(pady=6)
        ttk.Button(painel, text="Fechar", command=janela.destroy).pack(pady=(16, 0))
        janela.update_idletasks()
        janela.geometry(f"+{self.winfo_rootx() + max(0, (self.winfo_width()-janela.winfo_reqwidth())//2)}"
                       f"+{self.winfo_rooty() + max(0, (self.winfo_height()-janela.winfo_reqheight())//2)}")

    def criar_interface(self):
        """Cria os elementos da janela."""

        # Layout principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        frm_principal = ttk.Frame(self, padding=10)
        frm_principal.grid(
            row=0, column=0, sticky="nsew"
        )

        frm_principal.columnconfigure(0, weight=0, minsize=245)
        frm_principal.columnconfigure(1, weight=1)
        frm_principal.rowconfigure(0, weight=1)
        frm_principal.rowconfigure(1, weight=0)

        # Painel esquerdo
        frm_figuras = ttk.LabelFrame(
            frm_principal,
            text="Figuras geométricas",
            padding=10
        )
        frm_figuras.grid(
            row=0, column=0,
            sticky="nsew",
            padx=(0, 8),
            pady=(0, 8)
        )

        frm_figuras.columnconfigure(0, weight=1)
        frm_figuras.rowconfigure(0, weight=1)

        self.lst_figuras = tk.Listbox(
            frm_figuras,
            height=15,
            exportselection=False
        )
        self.lst_figuras.grid(
            row=0, column=0,
            sticky="nsew"
        )
        self.lst_figuras.bind("<<ListboxSelect>>", self.destacar_figura_selecionada)

        barra_rolagem = ttk.Scrollbar(
            frm_figuras,
            orient="vertical",
            command=self.lst_figuras.yview
        )
        barra_rolagem.grid(
            row=0, column=1,
            sticky="ns"
        )

        self.lst_figuras.configure(
            yscrollcommand=barra_rolagem.set
        )

        frm_botoes = ttk.Frame(frm_figuras)
        frm_botoes.grid(
            row=1, column=0,
            columnspan=2,
            sticky="ew",
            pady=(10, 0)
        )

        ttk.Button(
            frm_botoes,
            text="Adicionar figura",
            command=self.adicionar_figura
        ).pack(fill="x", pady=3)

        ttk.Button(
            frm_botoes,
            text="Editar figura",
            command=self.editar_figura
        ).pack(fill="x", pady=3)

        ttk.Button(
            frm_botoes,
            text="Excluir figura",
            command=self.excluir_figura
        ).pack(fill="x", pady=3)

        ttk.Separator(frm_botoes, orient="horizontal").pack(fill="x", pady=8)

        ttk.Button(
            frm_botoes,
            text="Carregar exemplo",
            command=self.carregar_exemplo
        ).pack(fill="x", pady=3)

        ttk.Button(
            frm_botoes,
            text="Exibir todos os objetos",
            command=self.exibir_todos_objetos
        ).pack(fill="x", pady=3)

        ttk.Button(
            frm_botoes,
            text="Limpar tudo",
            command=self.limpar_tudo
        ).pack(fill="x", pady=3)

        # Painel do gráfico
        self.frm_grafico = ttk.LabelFrame(
            frm_principal,
            text="Visualização da seção",
            padding=5
        )
        self.frm_grafico.grid(
            row=0, column=1,
            sticky="nsew",
            pady=(0, 8)
        )

        self.frm_grafico.columnconfigure(0, weight=1)
        self.frm_grafico.rowconfigure(0, weight=0)
        self.frm_grafico.rowconfigure(1, weight=1)
        self.frm_grafico.rowconfigure(2, weight=0)

        frm_opcoes = ttk.Frame(self.frm_grafico)
        frm_opcoes.grid(row=0, column=0, sticky="ew", padx=8, pady=5)

        opcoes = [
            ("Eixos globais", self.mostrar_eixos),
            ("Centroide", self.mostrar_centroide),
            ("Eixos centroidais", self.mostrar_eixos_centrais),
            ("Eixos principais", self.mostrar_eixos_principais),
            ("Por partes", self.mostrar_por_partes),
            ("Círculo de Mohr", self.mostrar_mohr),
        ]
        for texto, variavel in opcoes:
            ttk.Checkbutton(
                frm_opcoes,
                text=texto,
                variable=variavel,
                command=self.atualizar_grafico,
            ).pack(side="left", padx=8)

        ttk.Checkbutton(
            frm_opcoes, text="Snap na grade", variable=self.snap_ativo,
            command=self._atualizar_preview_poligono,
        ).pack(side="left", padx=8)

        ttk.Checkbutton(
            frm_opcoes, text="Polígono negativo", variable=self.poligono_negativo,
        ).pack(side="left", padx=8)

        self.lbl_desenho = ttk.Label(frm_opcoes, text="")
        self.lbl_desenho.pack(side="left", padx=8)

        # Campos inferiores para controlar a malha dos eixos.
        frm_grade = ttk.Frame(self.frm_grafico)
        frm_grade.grid(row=2, column=0, sticky="w", padx=10, pady=(3, 6))

        ttk.Label(frm_grade, text="Espaçamento X:").pack(side="left", padx=(0, 4))
        ent_x = ttk.Entry(frm_grade, textvariable=self.espacamento_x, width=9)
        ent_x.pack(side="left", padx=(0, 18))

        ttk.Label(frm_grade, text="Espaçamento Y:").pack(side="left", padx=(0, 4))
        ent_y = ttk.Entry(frm_grade, textvariable=self.espacamento_y, width=9)
        ent_y.pack(side="left", padx=(0, 12))

        # Atualiza a grade automaticamente ao sair de qualquer campo.
        for entrada in (ent_x, ent_y):
            entrada.bind("<FocusOut>", lambda event: self.atualizar_grade())
            entrada.bind("<Return>", lambda event: self.atualizar_grade())

        # Painel inferior
        frm_resultados = ttk.LabelFrame(
            frm_principal,
            text="Propriedades geométricas",
            padding=10
        )
        frm_resultados.grid(
            row=1, column=0,
            columnspan=2,
            sticky="nsew"
        )

        frm_resultados.columnconfigure(0, weight=1)
        frm_resultados.rowconfigure(0, weight=1)

        self.txt_resultados = tk.Text(
            frm_resultados,
            height=10,
            font=("Consolas", 10),
            wrap="none",
            state="disabled",
            relief="flat",
            padx=8,
            pady=6,
        )
        self.txt_resultados.grid(row=0, column=0, sticky="nsew")


    def carregar_exemplo(self):
        """Carrega a seção composta de referência."""

        self.secao = SecaoComposta([
            Retangulo(
                b=120, h=140
            ),
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

        self.atualizar_interface()

    def limpar_tudo(self):
        """Remove todas as figuras e reinicia o desenho, após confirmação."""
        if not self.secao.figuras and not self.vertices_desenho:
            return
        if not messagebox.askyesno(
            "Limpar tudo",
            "Deseja remover todas as figuras e cancelar o desenho atual?",
            parent=self,
        ):
            return
        self.cancelar_poligono_mouse()
        self.secao = SecaoComposta()
        self.lst_figuras.selection_clear(0, tk.END)
        self.atualizar_interface()

    def exibir_todos_objetos(self):
        """Restaura o enquadramento de todas as figuras e atualiza a vista."""
        self.atualizar_interface()

    def atualizar_lista(self):
        """Atualiza a lista de figuras."""

        selecao_anterior = self.lst_figuras.curselection()
        self.lst_figuras.delete(0, tk.END)

        for i, figura in enumerate(
            self.secao.figuras, start=1
        ):
            tipo = type(figura).__name__

            operacao = (
                "+" if figura.sinal == 1 else "-"
            )

            descricao = (
                f"{i:02d}  {operacao}  {tipo}"
            )

            self.lst_figuras.insert(
                tk.END, descricao
            )

        if selecao_anterior and selecao_anterior[0] < self.lst_figuras.size():
            self.lst_figuras.selection_set(selecao_anterior[0])

    def destacar_figura_selecionada(self, event=None):
        """Destaca o contorno da figura escolhida, sem recriar o canvas."""
        for artista in self._contornos_selecao:
            artista.remove()
        self._contornos_selecao.clear()

        if self.figura_mpl is None or self.canvas_mpl is None:
            return

        selecao = self.lst_figuras.curselection()
        if not selecao or selecao[0] >= len(self.secao.figuras):
            self.canvas_mpl.draw_idle()
            return

        figura = self.secao.figuras[selecao[0]]
        ax = self.figura_mpl.axes[0]

        # Reutiliza o próprio renderizador geométrico para obter o contorno,
        # incluindo rotações, curvas e polígonos, sem duplicar fórmulas.
        figura_temporaria = None
        try:
            # Desenhar uma cópia positiva: a figura negativa isolada gera geometria vazia.
            figura_contorno = copy.copy(figura)
            figura_contorno.sinal = 1
            figura_temporaria, ax_temp = desenhar_secao(
                SecaoComposta([figura_contorno]),
                mostrar_componentes=False,
                mostrar_eixos=False,
                mostrar_centroide=False,
                mostrar_eixos_centrais=False,
                mostrar_eixos_principais=False,
                mostrar_propriedades=False,
            )
            caminhos = []
            for patch in ax_temp.patches:
                caminhos.append(patch.get_path().transformed(patch.get_transform()).transformed(ax_temp.transData.inverted()))
            for colecao in ax_temp.collections:
                for caminho in colecao.get_paths():
                    # As coleções geradas pelo preenchimento usam coordenadas de dados.
                    caminhos.append(caminho)

            for caminho in caminhos:
                contorno = PathPatch(
                    caminho, facecolor="none", edgecolor="red",
                    linewidth=2.5, zorder=100, joinstyle="round",
                )
                ax.add_patch(contorno)
                self._contornos_selecao.append(contorno)
        finally:
            if figura_temporaria is not None:
                plt.close(figura_temporaria)

        self.canvas_mpl.draw_idle()

    def _proporcao_area_grafica(self):
        """Razão largura/altura da área útil do gráfico, em pixels."""
        if self.canvas_mpl is None:
            return 1.0
        ax = self.figura_mpl.axes[0]
        largura, altura = ax.get_window_extent().size
        return largura / altura if altura > 0 else 1.0

    def _ajustar_escala_grafica(self, manter_altura=True):
        """Mantém uma unidade X com o mesmo tamanho visual de uma unidade Y.

        Os eixos ocupam todo o painel; a escala é preservada pelos limites,
        e não pelo encolhimento automático da caixa dos eixos.
        """
        if self.figura_mpl is None:
            return
        ax = self.figura_mpl.axes[0]
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        proporcao = self._proporcao_area_grafica()
        if manter_altura:
            largura_dados = (y1 - y0) * proporcao
            centro = (x0 + x1) / 2
            ax.set_xlim(centro - largura_dados / 2, centro + largura_dados / 2)
        else:
            altura_dados = (x1 - x0) / proporcao
            centro = (y0 + y1) / 2
            ax.set_ylim(centro - altura_dados / 2, centro + altura_dados / 2)
        ax.set_autoscale_on(False)

    def _zoom_scroll(self, event):
        """Zoom centrado no cursor, mantendo a escala X/Y uniforme."""
        if self.figura_mpl is None or self.canvas_mpl is None:
            return
        ax = self.figura_mpl.axes[0]
        if event.inaxes is not ax or event.xdata is None or event.ydata is None:
            return
        if event.button == "up":
            escala = 1 / 1.2
        elif event.button == "down":
            escala = 1.2
        else:
            return
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        px, py = event.xdata, event.ydata
        ax.set_xlim(px + (x0 - px) * escala, px + (x1 - px) * escala)
        ax.set_ylim(py + (y0 - py) * escala, py + (y1 - py) * escala)
        ax.set_autoscale_on(False)
        self.canvas_mpl.draw_idle()

    def _ajustar_tamanho_grafico(self, event=None):
        """Preenche o canvas e preserva a escala ao maximizar a janela."""
        if self.figura_mpl is None or self.canvas_mpl is None:
            return
        widget = self.canvas_mpl.get_tk_widget()
        largura, altura = widget.winfo_width(), widget.winfo_height()
        if largura <= 2 or altura <= 2:
            return
        # A troca de Figure não redimensiona automaticamente a PhotoImage
        # interna do FigureCanvasTkAgg. Redimensionar somente a Figure deixa
        # a imagem antiga no canto esquerdo e uma faixa branca à direita.
        # resize() atualiza a Figure E a imagem Tk com o tamanho real do widget.
        self.canvas_mpl.resize(SimpleNamespace(width=largura, height=altura))
        ax = self.figura_mpl.axes[0]
        ax.set_position([0.035, 0.045, 0.95, 0.93])
        ax.set_aspect("auto")
        self._ajustar_escala_grafica(manter_altura=True)
        self.canvas_mpl.draw_idle()

    def _redimensionamento_solicitado(self, event):
        """Evita redesenhos excessivos enquanto a janela é redimensionada."""
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(90, self._finalizar_redimensionamento)

    def _finalizar_redimensionamento(self):
        self._resize_job = None
        self._ajustar_tamanho_grafico()

    def atualizar_grafico(self):
        """Redesenha a seção mantendo as grades e as opções selecionadas."""
        if not self.secao.figuras:
            # Seção vazia: evita cálculos de centroide/inércia indefinidos.
            nova_figura, ax = plt.subplots()
            ax.set_xlim(-50, 50)
            ax.set_ylim(-50, 50)
            # Mesmo sem figuras, os eixos globais devem permanecer visíveis
            # quando a opção correspondente estiver marcada.
            if self.mostrar_eixos.get():
                ax.axhline(0, color="0.35", linewidth=0.8, alpha=0.75, zorder=2)
                ax.axvline(0, color="0.35", linewidth=0.8, alpha=0.75, zorder=2)
        else:
            nova_figura, ax = desenhar_secao(
                self.secao,
                mostrar_componentes=False,
                mostrar_eixos=self.mostrar_eixos.get(),
                mostrar_centroide=self.mostrar_centroide.get(),
                mostrar_eixos_centrais=self.mostrar_eixos_centrais.get(),
                mostrar_eixos_principais=self.mostrar_eixos_principais.get(),
                mostrar_propriedades=False,
            )
        # Os valores ficam reunidos no canto superior direito do gráfico,
        # sem sobrepor textos aos centroides das figuras.
        linhas_info = []
        if self.secao.figuras and self.mostrar_eixos_principais.get():
            imax, imin, _ = self.secao.inercias_principais()
            linhas_info.extend((f'Iu = {imax:.4g}', f'Iv = {imin:.4g}'))

        if self.mostrar_por_partes.get():
            xlim, ylim = ax.get_xlim(), ax.get_ylim()
            dimensao = max(xlim[1] - xlim[0], ylim[1] - ylim[0])
            raio_eixos = 0.045 * dimensao
            if linhas_info:
                linhas_info.append('')
            for indice, figura in enumerate(self.secao.figuras, start=1):
                xc_p, yc_p = figura.centroide()
                ax.plot([xc_p - raio_eixos, xc_p + raio_eixos],
                        [yc_p, yc_p], '--', color='tab:blue', lw=1.2, zorder=11)
                ax.plot([xc_p, xc_p],
                        [yc_p - raio_eixos, yc_p + raio_eixos],
                        '--', color='tab:blue', lw=1.2, zorder=11)
                ax.plot(xc_p, yc_p, 'x', color='tab:blue',
                        markersize=7, markeredgewidth=1.5, zorder=12)
                ax.annotate(f'C{indice}', xy=(xc_p, yc_p), xytext=(6, 6),
                            textcoords='offset points', fontsize=8,
                            color='tab:blue', zorder=13)

                # Para os vazios, as propriedades são exibidas como
                # grandezas geométricas positivas; o sinal é identificado.
                figura_positiva = copy.copy(figura)
                figura_positiva.sinal = 1
                area_p = figura_positiva.area()
                if hasattr(figura_positiva, 'inercias_centrais'):
                    ix_p, iy_p, ixy_p = figura_positiva.inercias_centrais()
                else:
                    ix_p, iy_p, ixy_p = figura_positiva.inercias_eixos()
                tipo = ' (-)' if getattr(figura, 'sinal', 1) < 0 else ' (+)'
                linhas_info.extend((
                    f'Parte {indice}{tipo}: C({xc_p:.1f}, {yc_p:.1f})',
                    f'  A = {area_p:.4g}',
                    f'  Ix = {ix_p:.4g}   Iy = {iy_p:.4g}',
                    f'  Ixy = {ixy_p:.4g}',
                ))

        if linhas_info:
            ax.text(0.985, 0.985, '\n'.join(linhas_info),
                    transform=ax.transAxes, ha='right', va='top',
                    fontsize=8, color='tab:blue', zorder=14,
                    bbox=dict(boxstyle='round,pad=0.4',
                              facecolor='white', alpha=0.85,
                              edgecolor='0.75'))

        # O título pertence à janela Tkinter, não ao gráfico.
        ax.set_title("")

        try:
            passo_x = float(self.espacamento_x.get().strip().replace(",", "."))
            passo_y = float(self.espacamento_y.get().strip().replace(",", "."))
            if not (0 < passo_x < float("inf") and 0 < passo_y < float("inf")):
                raise ValueError
        except ValueError:
            plt.close(nova_figura)
            messagebox.showerror(
                "Espaçamento inválido",
                "Informe espaçamentos positivos e finitos para X e Y.",
                parent=self,
            )
            return

        ax.xaxis.set_major_locator(MultipleLocator(passo_x))
        ax.yaxis.set_major_locator(MultipleLocator(passo_y))
        ax.grid(True, which="major", linestyle=":", alpha=0.35)

        # Oculta letras, valores e marcas das coordenadas, preservando a grade.
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.tick_params(axis="both", which="both",
                       labelbottom=False, labelleft=False,
                       labeltop=False, labelright=False, length=0)
        # A proporção geométrica será garantida pelos limites dos eixos.
        # A caixa dos eixos pode, portanto, preencher toda a janela.
        ax.set_aspect("auto")
        ax.set_position([0.035, 0.045, 0.95, 0.93])

        # O widget Tk do canvas é criado somente na primeira plotagem.
        # Nas demais, substituímos apenas a Figure associada ao canvas,
        # sem destruir o widget (evita o clarão causado pela recriação).
        if self.canvas_mpl is None:
            self.figura_mpl = nova_figura
            self.canvas_mpl = FigureCanvasTkAgg(
                self.figura_mpl, master=self.frm_grafico
            )
            self.canvas_mpl.mpl_connect("scroll_event", self._zoom_scroll)
            self._conectar_eventos_poligono()
            widget = self.canvas_mpl.get_tk_widget()
            widget.grid(row=1, column=0, sticky="nsew")
            widget.bind("<Configure>", self._redimensionamento_solicitado)
            self.after_idle(self._ajustar_tamanho_grafico)
        else:
            figura_anterior = self.figura_mpl
            largura, altura = self.figura_mpl.get_size_inches()
            nova_figura.set_size_inches(largura, altura, forward=False)
            self.canvas_mpl.figure = nova_figura
            nova_figura.set_canvas(self.canvas_mpl)
            self.figura_mpl = nova_figura
            # Os callbacks do Matplotlib pertencem à Figure; reconectar
            # após sua substituição para manter o zoom funcionando.
            self.canvas_mpl.mpl_connect("scroll_event", self._zoom_scroll)
            self._conectar_eventos_poligono()
            plt.close(figura_anterior)

        # Recria o traçado provisório na figura atual, se necessário.
        self.artistas_desenho = []
        if self.modo_poligono:
            self._atualizar_preview_poligono()

        # Sincroniza o tamanho do bitmap Tk após trocar a Figure.
        # Apenas alterar Figure.set_size_inches não expande o bitmap exibido.
        self._ajustar_tamanho_grafico()
        self._contornos_selecao.clear()
        self.destacar_figura_selecionada()
        self.canvas_mpl.draw_idle()
        self.atualizar_mohr()

    def _conectar_eventos_poligono(self):
        """Registra eventos na Figure atual (trocas invalidam os anteriores)."""
        self.canvas_mpl.mpl_connect("button_press_event", self._clique_poligono)
        self.canvas_mpl.mpl_connect("motion_notify_event", self._movimento_poligono)
        self.canvas_mpl.mpl_connect("key_press_event", self._tecla_poligono)

    def _ponto_snap(self, x, y):
        """Snap para a interseção mais próxima da grade configurada."""
        if not self.snap_ativo.get():
            return (float(x), float(y))
        try:
            dx = float(self.espacamento_x.get().strip().replace(",", "."))
            dy = float(self.espacamento_y.get().strip().replace(",", "."))
            if not (math.isfinite(dx) and math.isfinite(dy) and dx > 0 and dy > 0):
                raise ValueError
        except ValueError:
            return (float(x), float(y))
        return (math.floor(x / dx + 0.5) * dx,
                math.floor(y / dy + 0.5) * dy)

    def _proximo_do_primeiro_vertice(self, ponto, tolerancia_px=12):
        """Com snap desligado, detecta proximidade em pixels (independe do zoom)."""
        if self.snap_ativo.get() or not self.vertices_desenho or self.figura_mpl is None:
            return False
        ax = self.figura_mpl.axes[0]
        p0 = ax.transData.transform(self.vertices_desenho[0])
        p1 = ax.transData.transform(ponto)
        return math.dist(p0, p1) <= tolerancia_px

    def iniciar_poligono_mouse(self):
        """Inicia automaticamente o polígono no primeiro clique esquerdo."""
        self.sinal_poligono = -1 if self.poligono_negativo.get() else 1
        self.vertices_desenho = []
        self.modo_poligono = True
        self.lbl_desenho.configure(
            text="Desenhando: direito/Enter conclui; Esc cancela"
        )
        if self.canvas_mpl is not None:
            self.canvas_mpl.get_tk_widget().focus_set()

    def _clique_poligono(self, event):
        if not self.modo_poligono and event.button == 1 and event.inaxes is self.figura_mpl.axes[0]:
            self.iniciar_poligono_mouse()
        if not self.modo_poligono:
            return
        if event.button == 3:
            self.concluir_poligono_mouse()
            return
        if event.button != 1 or event.inaxes is not self.figura_mpl.axes[0]:
            return
        if event.xdata is None or event.ydata is None:
            return
        ponto = self._ponto_snap(event.xdata, event.ydata)
        if self.vertices_desenho and math.dist(ponto, self.vertices_desenho[-1]) < 1e-9:
            return
        # Clique no primeiro vértice fecha a figura, se houver ao menos três.
        if len(self.vertices_desenho) >= 3 and (math.dist(ponto, self.vertices_desenho[0]) < 1e-9 or self._proximo_do_primeiro_vertice(ponto)):
            self.concluir_poligono_mouse()
            return
        self.vertices_desenho.append(ponto)
        self._atualizar_preview_poligono()

    def _movimento_poligono(self, event):
        if not self.modo_poligono or event.inaxes is not self.figura_mpl.axes[0]:
            return
        if event.xdata is None or event.ydata is None:
            return
        ponto = self._ponto_snap(event.xdata, event.ydata)
        if len(self.vertices_desenho) >= 3 and self._proximo_do_primeiro_vertice(ponto):
            ponto = self.vertices_desenho[0]
        self._atualizar_preview_poligono(ponto)

    def _tecla_poligono(self, event):
        if not self.modo_poligono:
            return
        if event.key in ("escape", "esc"):
            self.cancelar_poligono_mouse()
        elif event.key in ("enter", "return"):
            self.concluir_poligono_mouse()
        elif event.key in ("backspace", "delete") and self.vertices_desenho:
            self.vertices_desenho.pop()
            self._atualizar_preview_poligono()

    def _atualizar_preview_poligono(self, cursor=None):
        if self.figura_mpl is None or self.canvas_mpl is None:
            return
        for artista in self.artistas_desenho:
            try:
                artista.remove()
            except (ValueError, NotImplementedError):
                pass
        self.artistas_desenho.clear()
        if not self.modo_poligono:
            self.canvas_mpl.draw_idle()
            return
        pontos = list(self.vertices_desenho)
        if cursor is not None and (not pontos or math.dist(cursor, pontos[-1]) > 1e-9):
            pontos.append(cursor)
        if pontos:
            ax = self.figura_mpl.axes[0]
            linha, = ax.plot([p[0] for p in pontos], [p[1] for p in pontos],
                             color="crimson", linestyle="--", linewidth=1.7,
                             marker="o", markersize=5, zorder=30)
            self.artistas_desenho.append(linha)
            if len(self.vertices_desenho) >= 3:
                linha_fecho, = ax.plot([pontos[-1][0], pontos[0][0]],
                                      [pontos[-1][1], pontos[0][1]],
                                      color="crimson", linestyle=":", zorder=29)
                self.artistas_desenho.append(linha_fecho)
        self.canvas_mpl.draw_idle()

    def cancelar_poligono_mouse(self):
        self.modo_poligono = False
        self.vertices_desenho = []
        self.lbl_desenho.configure(text="")
        self._atualizar_preview_poligono()

    def concluir_poligono_mouse(self):
        if not self.modo_poligono:
            return
        pontos = list(self.vertices_desenho)
        if len(pontos) < 3:
            messagebox.showwarning("Polígono", "Marque pelo menos três vértices.", parent=self)
            return
        area_assinada = sum(pontos[i][0] * pontos[(i+1)%len(pontos)][1]
                             - pontos[(i+1)%len(pontos)][0] * pontos[i][1]
                             for i in range(len(pontos))) / 2
        if abs(area_assinada) < 1e-10:
            messagebox.showerror("Polígono", "Os vértices formam uma área nula.", parent=self)
            return
        try:
            figura = Poligono(pontos, x0=0, y0=0, theta=0,
                             sinal=self.sinal_poligono)
            self.secao.adicionar(figura)
            self.cancelar_poligono_mouse()
            self.atualizar_interface()
        except (ValueError, TypeError) as erro:
            messagebox.showerror("Polígono inválido", str(erro), parent=self)

    def atualizar_grade(self):
        """Atualiza somente os localizadores da grade, sem recriar o gráfico."""
        try:
            passo_x = float(self.espacamento_x.get().strip().replace(",", "."))
            passo_y = float(self.espacamento_y.get().strip().replace(",", "."))
            if not (0 < passo_x < float("inf") and 0 < passo_y < float("inf")):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Espaçamento inválido",
                "Informe espaçamentos positivos e finitos para X e Y.",
                parent=self,
            )
            return

        if self.figura_mpl is None or self.canvas_mpl is None:
            return
        ax = self.figura_mpl.axes[0]
        ax.xaxis.set_major_locator(MultipleLocator(passo_x))
        ax.yaxis.set_major_locator(MultipleLocator(passo_y))
        self.canvas_mpl.draw_idle()

    def atualizar_resultados(self):
        """Exibe os resultados em texto, coerentes com as unidades de entrada."""
        if not self.secao.figuras:
            self.txt_resultados.configure(state="normal")
            self.txt_resultados.delete("1.0", tk.END)
            self.txt_resultados.insert("1.0", "Nenhuma figura adicionada.")
            self.txt_resultados.configure(state="disabled")
            return
        A = self.secao.area()
        xc, yc = self.secao.centroide()
        Ix, Iy, Ixy = self.secao.inercias_centrais()
        Imax, Imin, angulo = self.secao.inercias_principais()

        texto = (
            f"Área total:       {A:14.3f}\n"
            f"Centroide xc:     {xc:14.3f}\n"
            f"Centroide yc:     {yc:14.3f}\n"
            f"Ix central:       {Ix:14.3e}\n"
            f"Iy central:       {Iy:14.3e}\n"
            f"Ixy central:      {Ixy:14.3e}\n"
            f"Iu:               {Imax:14.3e}\n"
            f"Iv:               {Imin:14.3e}\n"
            f"Ângulo principal: {angulo:14.3f}\n\n"
            "Consistência dimensional: resultados nas unidades derivadas das entradas."
        )
        self.txt_resultados.configure(state="normal")
        self.txt_resultados.delete("1.0", tk.END)
        self.txt_resultados.insert("1.0", texto)
        self.txt_resultados.configure(state="disabled")

    def _fechar_mohr(self):
        """Fecha a janela do círculo e desmarca a opção."""
        self.mostrar_mohr.set(False)
        if self.figura_mohr is not None:
            plt.close(self.figura_mohr)
        self.figura_mohr = None
        self.canvas_mohr = None
        if self.janela_mohr is not None:
            self.janela_mohr.destroy()
        self.janela_mohr = None

    def atualizar_mohr(self):
        """Exibe o círculo de Mohr das inércias em janela independente."""
        if not self.mostrar_mohr.get():
            if self.janela_mohr is not None:
                self._fechar_mohr()
            return

        if self.janela_mohr is None or not self.janela_mohr.winfo_exists():
            self.janela_mohr = tk.Toplevel(self)
            self.janela_mohr.title("PyComposta — Círculo de Mohr")
            self.janela_mohr.geometry("720x610")
            self.janela_mohr.protocol("WM_DELETE_WINDOW", self._fechar_mohr)
            self.figura_mohr, ax = plt.subplots(figsize=(7, 5.7))
            self.canvas_mohr = FigureCanvasTkAgg(self.figura_mohr, master=self.janela_mohr)
            self.canvas_mohr.get_tk_widget().pack(fill="both", expand=True)
        else:
            self.figura_mohr.clear()
            ax = self.figura_mohr.add_subplot(111)

        if not self.secao.figuras:
            ax.text(0.5, 0.5, "Adicione figuras para visualizar o círculo de Mohr.",
                    ha="center", va="center", transform=ax.transAxes)
            ax.set_axis_off()
        else:
            ix, iy, ixy = self.secao.inercias_centrais()
            iu, iv, angulo = self.secao.inercias_principais()
            centro = (ix + iy) / 2
            raio = math.hypot((ix - iy) / 2, ixy)
            from matplotlib.patches import Circle
            ax.add_patch(Circle((centro, 0), raio, fill=False,
                                color="tab:blue", linewidth=2))
            ax.plot([ix, iy], [ixy, -ixy], "o--", color="tab:orange", lw=1.3)
            ax.plot([iv, iu], [0, 0], "o", color="tab:green")
            ax.plot(centro, 0, "x", color="black", markersize=9, zorder=5)
            # Centro e raio indicados diretamente no diagrama.
            ax.annotate("C", (centro, 0), xytext=(6, -17),
                        textcoords="offset points", fontsize=10, fontweight="bold")
            if raio > 0:
                from matplotlib.patches import Arc
                # O raio é traçado até o ponto correspondente ao eixo x.
                ax.plot([centro, ix], [0, ixy], color="tab:purple",
                        linewidth=1.8, zorder=3)
                ax.annotate("R", ((centro + ix) / 2, ixy / 2),
                            xytext=(7, 6), textcoords="offset points",
                            color="tab:purple", fontsize=10, fontweight="bold")
                # Ângulo no plano de Mohr: da direção horizontal positiva
                # ao raio que passa pelo ponto (Ix, Ixy).
                phi = math.degrees(math.atan2(ixy, ix - centro))
                raio_arco = raio * 0.24
                inicio, fim = (0, phi) if phi >= 0 else (phi, 0)
                ax.add_patch(Arc((centro, 0), 2 * raio_arco, 2 * raio_arco,
                                 theta1=inicio, theta2=fim,
                                 color="tab:red", linewidth=1.7, zorder=4))
                angulo_meio = math.radians(phi / 2)
                ax.annotate(f"2θ = {phi:.1f}°",
                            (centro + raio_arco * 1.5 * math.cos(angulo_meio),
                             raio_arco * 1.5 * math.sin(angulo_meio)),
                            color="tab:red", fontsize=9, ha="center", va="center")
            ax.annotate("(Ix, Ixy)", (ix, ixy), xytext=(7, 8),
                        textcoords="offset points", fontsize=9)
            ax.annotate("(Iy, -Ixy)", (iy, -ixy), xytext=(7, -16),
                        textcoords="offset points", fontsize=9)
            ax.annotate("Iv", (iv, 0), xytext=(-12, 9),
                        textcoords="offset points", fontsize=9)
            ax.annotate("Iu", (iu, 0), xytext=(5, 9),
                        textcoords="offset points", fontsize=9)
            ax.axhline(0, color="0.35", linewidth=0.8)
            ax.axvline(0, color="0.75", linewidth=0.8)
            folga = max(raio * 0.3, abs(centro) * 0.025, 1.0)
            ax.set_xlim(centro - raio - folga, centro + raio + folga)
            ax.set_ylim(-raio - folga, raio + folga)
            ax.set_aspect("equal", adjustable="box")
            ax.set_xlabel("Momento de inércia, I")
            ax.set_ylabel("Produto de inércia, Ixy")
            ax.set_title("Círculo de Mohr das propriedades geométricas")
            ax.grid(True, linestyle=":", alpha=0.4)
            ax.text(0.02, 0.98,
                    f"C = ({centro:.5g}, 0)    R = {raio:.5g}\n"
                    f"Iu = {iu:.5g}    Iv = {iv:.5g}\n"
                    f"θ principal = {angulo:.3f}° (na seção)",
                    transform=ax.transAxes, va="top", fontsize=9,
                    bbox=dict(facecolor="white", alpha=0.85, edgecolor="0.8"))
        self.figura_mohr.tight_layout()
        self.canvas_mohr.draw_idle()

    def fechar_aplicacao(self):
        """Libera o gráfico e encerra a janela principal."""
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
            self._resize_job = None
        if self.figura_mpl is not None:
            plt.close(self.figura_mpl)
            self.figura_mpl = None
        if self.janela_mohr is not None:
            self._fechar_mohr()
        self.quit()
        self.destroy()

    def atualizar_interface(self):
        """Atualiza os três painéis."""

        try:
            self.atualizar_lista()
            self.atualizar_grafico()
            self.atualizar_resultados()

        except Exception as erro:
            messagebox.showerror(
                "Erro no PyComposta",
                str(erro)
            )

    def adicionar_figura(self):
        """Abre o formulário para criar uma figura."""

        formulario = FormularioFigura(self)
        self.wait_window(formulario)

        if formulario.resultado is not None:
            self.secao.adicionar(formulario.resultado)
            self.atualizar_interface()

    def editar_figura(self):
        """Edita a figura selecionada."""

        selecao = self.lst_figuras.curselection()

        if not selecao:
            messagebox.showwarning(
                "Seleção",
                "Selecione uma figura para editar."
            )
            return

        indice = selecao[0]
        figura = self.secao.figuras[indice]

        formulario = FormularioFigura(
            self, figura=figura
        )
        self.wait_window(formulario)

        if formulario.resultado is not None:
            self.secao.figuras[indice] = (
                formulario.resultado
            )
            self.atualizar_interface()

    def excluir_figura(self):
        """Exclui a figura selecionada."""

        selecao = self.lst_figuras.curselection()

        if not selecao:
            messagebox.showwarning(
                "Seleção",
                "Selecione uma figura para excluir."
            )
            return

        confirmar = messagebox.askyesno(
            "Excluir figura",
            "Deseja realmente excluir a figura?"
        )

        if confirmar:
            indice = selecao[0]
            del self.secao.figuras[indice]
            self.atualizar_interface()


if __name__ == "__main__":
    app = InterfacePyComposta()
    app.mainloop()
