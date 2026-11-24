
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


# Carregar arquivos
try:
    arquivo = open("produtos.json", "r", encoding="utf-8")
    produtos = json.load(arquivo)
    arquivo.close()
except:
    produtos = []

try:
    arquivo = open("movimentacoes.json", "r", encoding="utf-8")
    movimentacoes = json.load(arquivo)
    arquivo.close()
except:
    movimentacoes = []


# Salvar arquivos
def salvar():
    arquivo = open("produtos.json", "w", encoding="utf-8")
    json.dump(produtos, arquivo, indent=4, ensure_ascii=False)
    arquivo.close()

    arquivo = open("movimentacoes.json", "w", encoding="utf-8")
    json.dump(movimentacoes, arquivo, indent=4, ensure_ascii=False)
    arquivo.close()


# Mostrar produtos
def mostrar(filtro="todos"):
    tabela.delete(*tabela.get_children())

    for p in produtos:
        if filtro == "baixo" and p["quantidade"] > p["estoque_minimo"]:
            continue

        if filtro == "pesquisa":
            busca = caixa.get().lower()
            if busca not in p["nome"].lower() and busca not in str(p["codigo"]):
                continue

        tabela.insert("", tk.END, values=(
            p["codigo"], p["nome"], p["quantidade"],
            p["estoque_minimo"], "R$ {:.2f}".format(p["preco"])
        ))


# Cadastrar produto
def cadastrar():
    try:
        cod = int(codigo.get())
        nom = nome.get().strip()
        qtd = int(quantidade.get())
        minimo_estoque = int(minimo.get())
        valor = float(preco.get().replace(",", "."))

        if cod <= 0 or nom == "" or qtd < 0 or minimo_estoque < 0 or valor <= 0:
            messagebox.showwarning("Aviso", "Verifique os dados.")
            return

        for p in produtos:
            if p["codigo"] == cod:
                messagebox.showwarning("Aviso", "Código já cadastrado.")
                return

        produtos.append({
            "codigo": cod,
            "nome": nom,
            "quantidade": qtd,
            "estoque_minimo": minimo_estoque,
            "preco": valor
        })

        salvar()
        mostrar()

        codigo.delete(0, tk.END)
        nome.delete(0, tk.END)
        quantidade.delete(0, tk.END)
        minimo.delete(0, tk.END)
        preco.delete(0, tk.END)

        messagebox.showinfo("Sucesso", "Produto cadastrado!")

    except:
        messagebox.showerror("Erro", "Preencha os campos corretamente.")


# Selecionar produto
def selecionar(event):
    selecionado = tabela.selection()

    if selecionado:
        valores = tabela.item(selecionado[0], "values")

        codigo.delete(0, tk.END)
        nome.delete(0, tk.END)
        quantidade.delete(0, tk.END)
        minimo.delete(0, tk.END)
        preco.delete(0, tk.END)

        codigo.insert(0, valores[0])
        nome.insert(0, valores[1])
        quantidade.insert(0, valores[2])
        minimo.insert(0, valores[3])
        preco.insert(0, valores[4].replace("R$ ", ""))


# Alterar produto
def alterar():
    try:
        cod = int(codigo.get())
        nom = nome.get().strip()
        qtd = int(quantidade.get())
        minimo_estoque = int(minimo.get())
        valor = float(preco.get().replace(",", "."))

        if nom == "" or qtd < 0 or minimo_estoque < 0 or valor <= 0:
            messagebox.showwarning("Aviso", "Verifique os dados.")
            return

        for p in produtos:
            if p["codigo"] == cod:
                p["nome"] = nom
                p["quantidade"] = qtd
                p["estoque_minimo"] = minimo_estoque
                p["preco"] = valor

                salvar()
                mostrar()
                messagebox.showinfo("Sucesso", "Produto alterado!")
                return

        messagebox.showwarning("Aviso", "Produto não encontrado.")

    except:
        messagebox.showerror("Erro", "Verifique os campos.")


# Excluir produto
def excluir():
    try:
        cod = int(codigo.get())

        for p in produtos:
            if p["codigo"] == cod:
                if messagebox.askyesno("Confirmar", "Deseja excluir este produto?"):
                    produtos.remove(p)
                    salvar()
                    mostrar()

                    codigo.delete(0, tk.END)
                    nome.delete(0, tk.END)
                    quantidade.delete(0, tk.END)
                    minimo.delete(0, tk.END)
                    preco.delete(0, tk.END)
                return

        messagebox.showwarning("Aviso", "Produto não encontrado.")

    except:
        messagebox.showerror("Erro", "Informe um código válido.")


# Registrar entrada e saída
def movimentar(tipo):
    try:
        cod = int(codigo.get())
        qtd = int(quantidade_mov.get())

        if qtd <= 0:
            messagebox.showwarning("Aviso", "Quantidade inválida.")
            return

        for p in produtos:
            if p["codigo"] == cod:
                if tipo == "Entrada":
                    p["quantidade"] += qtd
                else:
                    if qtd > p["quantidade"]:
                        messagebox.showwarning("Aviso", "Estoque insuficiente.")
                        return
                    p["quantidade"] -= qtd

                movimentacoes.append({
                    "codigo": cod,
                    "produto": p["nome"],
                    "tipo": tipo,
                    "quantidade": qtd,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M")
                })

                salvar()
                mostrar()
                quantidade_mov.delete(0, tk.END)
                messagebox.showinfo("Sucesso", "Movimentação registrada!")
                return

        messagebox.showwarning("Aviso", "Produto não encontrado.")

    except:
        messagebox.showerror("Erro", "Informe o código e a quantidade.")


# Mostrar movimentações
def mostrar_movimentacoes():
    janela = tk.Toplevel(tela)
    janela.title("Movimentações")
    janela.geometry("650x350")

    tabela_mov = ttk.Treeview(
        janela,
        columns=("codigo", "produto", "tipo", "quantidade", "data"),
        show="headings"
    )

    tabela_mov.heading("codigo", text="Código")
    tabela_mov.heading("produto", text="Produto")
    tabela_mov.heading("tipo", text="Tipo")
    tabela_mov.heading("quantidade", text="Quantidade")
    tabela_mov.heading("data", text="Data")

    tabela_mov.pack(fill="both", expand=True)

    for m in movimentacoes:
        tabela_mov.insert("", tk.END, values=(
            m["codigo"], m["produto"], m["tipo"],
            m["quantidade"], m["data"]
        ))


# Janela principal
tela = tk.Tk()
tela.title("Sistema de Controle de Estoque")
tela.geometry("850x750")
tela.configure(bg="gray")


# Fundo e imagem
canvas = tk.Canvas(tela, width=850, height=750,
                   bg="gray", highlightthickness=0)

imagem = tk.PhotoImage(file="barra.png")
imagem = imagem.subsample(15, 10)


# Estilo dos botões
estilo = {
    "bg": "white",
    "fg": "black",
    "font": ("Arial", 10),
    "cursor": "hand2",
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 0,
    "activebackground": "white"
}


# Título
titulo = tk.Label(tela, text="Sistema de Controle de Estoque",
                  font=("Arial", 14, "bold"), bg="gray")
canvas.create_window(425, 30, window=titulo)


# Pesquisa
tk.Label(tela, text="Nome ou código:", font=("Arial", 12),
         bg="gray").place(x=360, y=65)

caixa = tk.Entry(tela, font=("Arial", 12))
caixa.place(x=350, y=90, width=150)


# Imagens dos botões superiores
for x in [40, 250, 460, 660]:
    canvas.create_image(x, 115, image=imagem, anchor="nw")


# Botões superiores
b1 = tk.Button(tela, text="Pesquisar", command=lambda: mostrar("pesquisa"), **estilo)
canvas.create_window(40 + imagem.width()/2, 115 + imagem.height()/2, window=b1)

b2 = tk.Button(tela, text="Estoque baixo", command=lambda: mostrar("baixo"), **estilo)
canvas.create_window(250 + imagem.width()/2, 115 + imagem.height()/2, window=b2)

b3 = tk.Button(tela, text="Listar todos", command=lambda: mostrar(), **estilo)
canvas.create_window(460 + imagem.width()/2, 115 + imagem.height()/2, window=b3)

b4 = tk.Button(tela, text="Movimentações", command=mostrar_movimentacoes, **estilo)
canvas.create_window(660 + imagem.width()/2, 115 + imagem.height()/2, window=b4)


# Campos do produto
tk.Label(tela, text="Código:", bg="gray").place(x=70, y=175)
codigo = tk.Entry(tela)
codigo.place(x=70, y=200, width=120)

tk.Label(tela, text="Nome:", bg="gray").place(x=220, y=175)
nome = tk.Entry(tela)
nome.place(x=220, y=200, width=120)

tk.Label(tela, text="Quantidade:", bg="gray").place(x=370, y=175)
quantidade = tk.Entry(tela)
quantidade.place(x=370, y=200, width=120)

tk.Label(tela, text="Estoque mínimo:", bg="gray").place(x=520, y=175)
minimo = tk.Entry(tela)
minimo.place(x=520, y=200, width=120)

tk.Label(tela, text="Preço:", bg="gray").place(x=670, y=175)
preco = tk.Entry(tela)
preco.place(x=670, y=200, width=120)


# Imagens dos botões de cadastro
for x in [200, 350, 500]:
    canvas.create_image(x, 245, image=imagem, anchor="nw")


# Botões de cadastro
b5 = tk.Button(tela, text="Cadastrar", command=cadastrar, **estilo)
canvas.create_window(200 + imagem.width()/2, 245 + imagem.height()/2, window=b5)

b6 = tk.Button(tela, text="Alterar", command=alterar, **estilo)
canvas.create_window(350 + imagem.width()/2, 245 + imagem.height()/2, window=b6)

b7 = tk.Button(tela, text="Excluir", command=excluir, **estilo)
canvas.create_window(500 + imagem.width()/2, 245 + imagem.height()/2, window=b7)


# Tabela de produtos
titulo_tabela = tk.Label(tela, text="Produtos cadastrados",
                         font=("Arial", 12, "bold"), bg="gray")
canvas.create_window(425, 325, window=titulo_tabela)

colunas = ("codigo", "nome", "quantidade", "minimo", "preco")
tabela = ttk.Treeview(tela, columns=colunas, show="headings", height=8)

tabela.heading("codigo", text="Código")
tabela.heading("nome", text="Nome")
tabela.heading("quantidade", text="Quantidade")
tabela.heading("minimo", text="Estoque mínimo")
tabela.heading("preco", text="Preço")

tabela.column("codigo", width=90, anchor="center")
tabela.column("nome", width=180, anchor="center")
tabela.column("quantidade", width=120, anchor="center")
tabela.column("minimo", width=140, anchor="center")
tabela.column("preco", width=120, anchor="center")

canvas.create_window(425, 455, window=tabela, width=700, height=230)
tabela.bind("<<TreeviewSelect>>", selecionar)


# Movimentação
tk.Label(tela, text="Selecione um produto na tabela e informe a quantidade:",
         font=("Arial", 11), bg="gray").place(x=220, y=600)

tk.Label(tela, text="Quantidade:", bg="gray").place(x=390, y=635)
quantidade_mov = tk.Entry(tela)
quantidade_mov.place(x=365, y=660, width=120)


# Imagens dos botões de entrada e saída
canvas.create_image(200, 685, image=imagem, anchor="nw")
canvas.create_image(500, 685, image=imagem, anchor="nw")

b8 = tk.Button(tela, text="Registrar entrada",
               command=lambda: movimentar("Entrada"), **estilo)
canvas.create_window(200 + imagem.width()/2, 685 + imagem.height()/2, window=b8)

b9 = tk.Button(tela, text="Registrar saída",
               command=lambda: movimentar("Saída"), **estilo)
canvas.create_window(500 + imagem.width()/2, 685 + imagem.height()/2, window=b9)


# Criar arquivos se não existirem
salvar()

# Mostrar produtos
mostrar()

canvas.pack()
tela.mainloop()
