"""
PROJETO DE COMPUTAÇÃO - GAAL
Construção algorítmica das cônicas
Tema (d): ELIPSE COM EIXO MAIOR HORIZONTAL (centro na origem)

Equação reduzida:  x²/a² + y²/b² = 1 ,  com a > b > 0

Fluxo do programa (Etapas 1 a 5 do PDF):
    ENTRADA        -> Etapa 1: ler a e b e validar
    PROCESSAMENTO  -> Etapa 2: calcular c, e e os pontos da curva
                      Etapa 3: armazenar os pontos (x, y)
    SAÍDA/GRÁFICO  -> Etapa 4: plotar a curva
                      Etapa 5: marcar e identificar os elementos no gráfico

Para rodar:
    pip3 install matplotlib
    python3 elipse.py
"""

import math
import os
import subprocess
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")               # só gera o arquivo, sem janela que trava o programa
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# ETAPA 1 - DEFINIÇÃO DOS PARÂMETROS (ENTRADA)
# ---------------------------------------------------------------------------
def validar(a, b):
    """Devolve uma mensagem de erro, ou None se a e b forem válidos."""
    if not (math.isfinite(a) and math.isfinite(b)):
        return "a e b devem ser números finitos."
    if a <= 0 or b <= 0:
        return "a e b devem ser positivos."
    if a == b:
        return "com a = b a curva é uma CIRCUNFERÊNCIA, não uma elipse."
    if a < b:
        return ("com a < b o eixo maior fica VERTICAL (outro tema). "
                "Para eixo maior horizontal é preciso a > b.")
    return None


def ler_numero(mensagem):
    """Lê um número do teclado (aceita vírgula ou ponto como decimal)."""
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            print("  -> Valor inválido, digite um número.")


def ler_parametros():
    print("=" * 56)
    print(" ELIPSE COM EIXO MAIOR HORIZONTAL:  x²/a² + y²/b² = 1")
    print("=" * 56)
    while True:
        a = ler_numero("a (semieixo maior, horizontal): ")
        b = ler_numero("b (semieixo menor, vertical):   ")
        erro = validar(a, b)
        if erro is None:
            return a, b
        print(f"  -> Inválido: {erro}\n")


# ---------------------------------------------------------------------------
# ETAPA 2 - CÁLCULOS
# ---------------------------------------------------------------------------
def calcular_elementos(a, b):
    """Valores derivados de a e b."""
    c = math.sqrt(a**2 - b**2)      # relação a² = b² + c²
    e = c / a                       # excentricidade, 0 < e < 1
    return {
        "a": a, "b": b, "c": c, "e": e,
        "centro": (0.0, 0.0),
        "vertices": [(-a, 0.0), (a, 0.0)],
        "covertices": [(0.0, -b), (0.0, b)],
        "focos": [(-c, 0.0), (c, 0.0)],
        "diretrizes": [-a**2 / c, a**2 / c],    # x = ± a²/c
    }


def calcular_pontos(a, b, n=400):
    t = np.linspace(0, 2 * np.pi, n)        # N valores igualmente espaçados
    x = a * np.cos(t)
    y = b * np.sin(t)
    # ETAPA 3 - ARMAZENAMENTO: matriz n x 2, cada linha é um par (x, y)
    return np.column_stack((x, y))


# ---------------------------------------------------------------------------
# FORMATAÇÃO DOS TEXTOS DO GRÁFICO
# ---------------------------------------------------------------------------
def f(v):
    return f"{round(v, 4) + 0.0:g}"


def p(ponto):
    return f"({f(ponto[0])}, {f(ponto[1])})"


def texto_equacao(a, b):
    return f"x²/{f(a**2)} + y²/{f(b**2)} = 1"


# ---------------------------------------------------------------------------
# ETAPA 4 + 5 - VISUALIZAÇÃO E IDENTIFICAÇÃO NO GRÁFICO
# ---------------------------------------------------------------------------
def plotar(pontos, el, arquivo="elipse.png"):
    a, b, c = el["a"], el["b"], el["c"]
    fig, ax = plt.subplots(figsize=(11, 7), layout="constrained")

    # Curva
    ax.plot(pontos[:, 0], pontos[:, 1], color="tab:blue", lw=2.5, label="Elipse")

    # Eixos da elipse
    ax.plot([-a, a], [0, 0], color="tab:green", lw=1.5, label="Eixo maior: y = 0")
    ax.plot([0, 0], [-b, b], color="tab:purple", lw=1.5, label="Eixo menor: x = 0")

    # Diretrizes (tracejadas). Elas ficam a a²/c do centro, fora da elipse.
    dist_diretriz = a**2 / c
    diretriz_visivel = dist_diretriz <= 4 * a    # se e for muito pequeno, ficam longe demais
    if diretriz_visivel:
        for i, xd in enumerate(el["diretrizes"]):
            ax.axvline(xd, color="tab:orange", ls="--", lw=1.3,
                       label=f"Diretrizes: x = ± {f(dist_diretriz)}" if i == 0 else None)

    # Pontos notáveis
    def marcar(ponto, rotulo, estilo, cor, desloc, alinhamento="center"):
        ax.plot(*ponto, estilo, color=cor, ms=9)
        ax.annotate(f"{rotulo}{p(ponto)}", ponto, textcoords="offset points",
                    xytext=desloc, ha=alinhamento, fontsize=9, color=cor)

    marcar(el["centro"], "C", "o", "black", (0, -16))
    marcar(el["vertices"][0], "V1", "s", "tab:green", (-8, -18))
    marcar(el["vertices"][1], "V2", "s", "tab:green", (8, -18))
    marcar(el["covertices"][0], "B1", "s", "tab:purple", (0, -18))
    marcar(el["covertices"][1], "B2", "s", "tab:purple", (0, 10))
    # F1 com texto à esquerda e F2 à direita, para não se sobreporem quando c é pequeno
    marcar(el["focos"][0], "F1", "*", "tab:red", (-4, 10), "right")
    marcar(el["focos"][1], "F2", "*", "tab:red", (4, 10), "left")

    # Limites: alargados para as diretrizes aparecerem
    meia_largura = (dist_diretriz if diretriz_visivel else a) * 1.15
    meia_altura = b * 1.6
    ax.set_xlim(-meia_largura, meia_largura)
    ax.set_ylim(-meia_altura, meia_altura)

    # Eixos cartesianos, grade e proporção igual
    ax.axhline(0, color="black", lw=0.7)
    ax.axvline(0, color="black", lw=0.7)
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal")          # sem isso a elipse sai distorcida
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(texto_equacao(a, b) + f"    (c = {f(c)}, e = {f(el['e'])})")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=9)

    if not diretriz_visivel:
        ax.text(0.5, 0.03, f"Diretrizes x = ± {f(dist_diretriz)} ficam fora da área",
                transform=ax.transAxes, ha="center", fontsize=9, color="tab:orange")

    fig.savefig(arquivo, dpi=150)
    plt.close(fig)
    print(f"\nGráfico salvo em '{arquivo}'.")


def abrir_imagem(arquivo):
    """Abre a imagem no visualizador padrão do sistema, sem esperar ele fechar."""
    try:
        if sys.platform == "win32":
            os.startfile(arquivo)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", arquivo])
        else:
            subprocess.Popen(["xdg-open", arquivo])
    except Exception:
        print("Não foi possível abrir a imagem automaticamente; abra o arquivo manualmente.")


# ---------------------------------------------------------------------------
# FUNÇÃO PRINCIPAL (pode ser chamada com argumentos ou pelo teclado)
# ---------------------------------------------------------------------------
def construir_elipse(a, b, arquivo="elipse.png", abrir=True):
    erro = validar(a, b)
    if erro:
        raise ValueError(erro)
    elementos = calcular_elementos(a, b)         # Etapa 2
    pontos = calcular_pontos(a, b)               # Etapas 2 e 3
    plotar(pontos, elementos, arquivo)           # Etapas 4 e 5
    if abrir:
        abrir_imagem(arquivo)
    return pontos, elementos


if __name__ == "__main__":
    a, b = ler_parametros()                      # Etapa 1
    construir_elipse(a, b)
