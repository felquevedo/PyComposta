
import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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

        self.criar_interface()
        self.carregar_exemplo()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.fechar_aplicacao
        )

    def criar_interface(self):
        """Cria os elementos da janela."""

        # Layout principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        frm_principal = ttk.Frame(self, padding=10)
        frm_principal.grid(
            row=0, column=0, sticky="nsew"
        )

        frm_principal.columnconfigure(0, weight=1)
        frm_principal.columnconfigure(1, weight=3)
        frm_principal.rowconfigure(0, weight=3)
        frm_principal.rowconfigure(1, weight=1)

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
            text="Atualizar",
            command=self.atualizar_interface
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
        self.frm_grafico.rowconfigure(0, weight=1)

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
            height=11,
            font=("Consolas", 10),
            wrap="none",
            state="disabled"
        )
        self.txt_resultados.grid(
            row=0, column=0,
            sticky="nsew"
        )

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

    def atualizar_lista(self):
        """Atualiza a lista de figuras."""

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

    def atualizar_grafico(self):
        """Atualiza o gráfico incorporado."""

        if self.canvas_mpl is not None:
            self.canvas_mpl.get_tk_widget().destroy()
            self.canvas_mpl = None

        if self.figura_mpl is not None:
            plt.close(self.figura_mpl)
            self.figura_mpl = None

        self.figura_mpl, ax = desenhar_secao(
            self.secao,
            mostrar_componentes=False,
            mostrar_propriedades=False
        )

        self.figura_mpl.set_size_inches(7, 6)

        self.canvas_mpl = FigureCanvasTkAgg(
            self.figura_mpl,
            master=self.frm_grafico
        )

        self.canvas_mpl.draw()

        self.canvas_mpl.get_tk_widget().grid(
            row=0, column=0,
            sticky="nsew"
        )

    def atualizar_resultados(self):
        """Atualiza o painel numérico."""

        A = self.secao.area()
        xc, yc = self.secao.centroide()

        Ix, Iy, Ixy = (
            self.secao.inercias_centrais()
        )

        Imax, Imin, angulo = (
            self.secao.inercias_principais()
        )

        texto = (
            f"Área total:       {A:14.3f}\n"
            f"Centroide xc:     {xc:14.3f}\n"
            f"Centroide yc:     {yc:14.3f}\n"
            f"Ix central:       {Ix:14.3e}\n"
            f"Iy central:       {Iy:14.3e}\n"
            f"Ixy central:      {Ixy:14.3e}\n"
            f"Imax:             {Imax:14.3e}\n"
            f"Imin:             {Imin:14.3e}\n"
            f"Ângulo principal: {angulo:14.3f}°"
        )

        self.txt_resultados.configure(
            state="normal"
        )

        self.txt_resultados.delete(
            "1.0", tk.END
        )

        self.txt_resultados.insert(
            tk.END, texto
        )

        self.txt_resultados.configure(
            state="disabled"
        )

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

    def fechar_aplicacao(self):
        """Encerra a interface e libera os recursos gráficos."""

        if self.figura_mpl is not None:
            plt.close(self.figura_mpl)
            self.figura_mpl = None

        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = InterfacePyComposta()
    app.mainloop()
