
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

#Arquivos
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


#Salvar os dados
def salvar():
    arquivo = open("produtos.json", "w", encoding="utf-8")
    json.dump(produtos, arquivo, indent=4, ensure_ascii=False)
    arquivo.close()

    arquivo = open("movimentacoes.json", "w", encoding="utf-8")
    json.dump(movimentacoes, arquivo, indent=4, ensure_ascii=False)
    arquivo.close()


#Limpar os campos
def limpar():
    codigo.delete(0, tk.END)
    nome.delete(0, tk.END)
    quantidade.delete(0, tk.END)
    minimo.delete(0, tk.END)
    preco.delete(0, tk.END)



#Mostrar produtos na tabela
def listar():
    tabela.delete(*tabela.get_children())

    for p in produtos:
        tabela.insert("", tk.END, values=(
            p["codigo"],
            p["nome"],
            p["quantidade"],
            p["estoque_minimo"],
            "R$ {:.2f}".format(p["preco"])
        ))


#Cadastrar produto
def cadastrar():
    try:
        cod = int(codigo.get())
        nom = nome.get()
        qtd = int(quantidade.get())
        est_min = int(minimo.get())
        valor = float(preco.get().replace(",", "."))

        if cod <= 0 or nom == "" or qtd < 0 or est_min < 0 or valor <= 0:
            messagebox.showwarning("Aviso", "Verifique os dados.")
            return

        for p in produtos:
            if p["codigo"] == cod:
                messagebox.showwarning("Aviso", "Código já cadastrado.")
                return

        produto = {
            "codigo": cod,
            "nome": nom,
            "quantidade": qtd,
            "estoque_minimo": est_min,
            "preco": valor
        }

        produtos.append(produto)
        salvar()
        listar()
        limpar()

        messagebox.showinfo("Sucesso", "Produto cadastrado!")

    except:
        messagebox.showerror("Erro", "Preencha os campos corretamente.")


#Selecionar produto na tabela
def selecionar(event):
    selecionado = tabela.selection()

    if selecionado:
        valores = tabela.item(selecionado[0], "values")

        limpar()

        codigo.insert(0, valores[0])
        nome.insert(0, valores[1])
        quantidade.insert(0, valores[2])
        minimo.insert(0, valores[3])
        preco.insert(0, valores[4].replace("R$ ", ""))


#Alterar produto
def alterar():
    try:
        cod = int(codigo.get())

        for p in produtos:
            if p["codigo"] == cod:
                p["nome"] = nome.get()
                p["quantidade"] = int(quantidade.get())
                p["estoque_minimo"] = int(minimo.get())
                p["preco"] = float(preco.get().replace(",", "."))

                salvar()
                listar()
                limpar()

                messagebox.showinfo("Sucesso", "Produto alterado!")
                return

        messagebox.showwarning("Aviso", "Produto não encontrado.")

    except:
        messagebox.showerror("Erro", "Verifique os campos.")



#Excluir produto
def excluir():
    try:
        cod = int(codigo.get())

        for p in produtos:
            if p["codigo"] == cod:
                resposta = messagebox.askyesno(
                    "Confirmar",
                    "Deseja excluir este produto?"
                )

                if resposta:
                    produtos.remove(p)
                    salvar()
                    listar()
                    limpar()

                return

        messagebox.showwarning("Aviso", "Produto não encontrado.")

    except:
        messagebox.showerror("Erro", "Informe o código do produto.")



#Pesquisar produto
def consultar():
    busca = pesquisa.get().lower()

    tabela.delete(*tabela.get_children())

    for p in produtos:
        if busca in p["nome"].lower() or busca in str(p["codigo"]):
            tabela.insert("", tk.END, values=(
                p["codigo"],
                p["nome"],
                p["quantidade"],
                p["estoque_minimo"],
                "R$ {:.2f}".format(p["preco"])
            ))



#Mostrar produtos com estoque baixo
def estoque_baixo():
    tabela.delete(*tabela.get_children())

    for p in produtos:
        if p["quantidade"] <= p["estoque_minimo"]:
            tabela.insert("", tk.END, values=(
                p["codigo"],
                p["nome"],
                p["quantidade"],
                p["estoque_minimo"],
                "R$ {:.2f}".format(p["preco"])
            ))


#Registrar entrada ou saída
def movimentar(tipo):
    try:
        cod = int(codigo.get())
        qtd = int(qtd_mov.get())

        if qtd <= 0:
            messagebox.showwarning("Aviso", "Quantidade inválida.")
            return

        for p in produtos:
            if p["codigo"] == cod:

                if tipo == "Entrada":
                    p["quantidade"] += qtd

                else:
                    if qtd > p["quantidade"]:
                        messagebox.showwarning(
                            "Aviso",
                            "Estoque insuficiente."
                        )
                        return

                    p["quantidade"] -= qtd

                registro = {
                    "codigo": cod,
                    "produto": p["nome"],
                    "tipo": tipo,
                    "quantidade": qtd,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M")
                }

                movimentacoes.append(registro)

                salvar()
                listar()

                qtd_mov.delete(0, tk.END)

                messagebox.showinfo("Sucesso", "Movimentação registrada!")
                return

        messagebox.showwarning("Aviso", "Produto não encontrado.")

    except:
        messagebox.showerror("Erro", "Informe o código e a quantidade.")

#Mostrar histórico de movimentações
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
            m["codigo"],
            m["produto"],
            m["tipo"],
            m["quantidade"],
            m["data"]
        ))

# INTERFACE DO PROGRAMA

tela = tk.Tk()
tela.title("Controle de Estoque")
tela.geometry("850x750")
tela.configure(bg="#EEEEEE")

# Título
tk.Label(
    tela,
    text="CONTROLE DE ESTOQUE",
    font=("Arial", 18, "bold"),
    bg="#EEEEEE"
).pack(pady=10)



#Cadastro de produtos
cadastro = tk.LabelFrame(
    tela,
    text="Cadastro de produtos",
    bg="#EEEEEE",
    padx=10,
    pady=10
)
cadastro.pack(fill="x", padx=15, pady=5)

tk.Label(cadastro, text="Código:", bg="#EEEEEE").grid(row=0, column=0)
codigo = tk.Entry(cadastro)
codigo.grid(row=0, column=1, padx=5, pady=5)

tk.Label(cadastro, text="Nome:", bg="#EEEEEE").grid(row=0, column=2)
nome = tk.Entry(cadastro)
nome.grid(row=0, column=3, padx=5, pady=5)

tk.Label(cadastro, text="Quantidade:", bg="#EEEEEE").grid(row=1, column=0)
quantidade = tk.Entry(cadastro)
quantidade.grid(row=1, column=1, padx=5, pady=5)

tk.Label(cadastro, text="Estoque mínimo:", bg="#EEEEEE").grid(row=1, column=2)
minimo = tk.Entry(cadastro)
minimo.grid(row=1, column=3, padx=5, pady=5)

tk.Label(cadastro, text="Preço:", bg="#EEEEEE").grid(row=2, column=0)
preco = tk.Entry(cadastro)
preco.grid(row=2, column=1, padx=5, pady=5)

tk.Button(cadastro, text="Cadastrar", command=cadastrar).grid(row=3, column=0, pady=8)
tk.Button(cadastro, text="Alterar", command=alterar).grid(row=3, column=1)
tk.Button(cadastro, text="Excluir", command=excluir).grid(row=3, column=2)
tk.Button(cadastro, text="Limpar", command=limpar).grid(row=3, column=3)


#Pesquisa
busca = tk.LabelFrame(
    tela,
    text="Pesquisar produtos",
    bg="#EEEEEE",
    padx=10,
    pady=8
)
busca.pack(fill="x", padx=15, pady=5)


tk.Label(busca, text="Nome ou código:", bg="#EEEEEE").pack(side="left")

pesquisa = tk.Entry(busca, width=25)
pesquisa.pack(side="left", padx=5)

tk.Button(busca, text="Pesquisar", command=consultar).pack(side="left", padx=3)
tk.Button(busca, text="Estoque baixo", command=estoque_baixo).pack(side="left", padx=3)
tk.Button(busca, text="Listar todos", command=listar).pack(side="left", padx=3)
tk.Button(busca, text="Movimentações", command=mostrar_movimentacoes).pack(side="left", padx=3)


#Tabela de produtos
frame_tabela = tk.LabelFrame(
    tela,
    text="Produtos cadastrados",
    bg="#EEEEEE",
    padx=5,
    pady=5
)
frame_tabela.pack(fill="both", expand=True, padx=15, pady=5)

tabela = ttk.Treeview(
    frame_tabela,
    columns=("codigo", "nome", "quantidade", "minimo", "preco"),
    show="headings"
)

tabela.heading("codigo", text="Código")
tabela.heading("nome", text="Produto")
tabela.heading("quantidade", text="Quantidade")
tabela.heading("minimo", text="Estoque mínimo")
tabela.heading("preco", text="Preço")

tabela.column("codigo", width=70)
tabela.column("nome", width=200)
tabela.column("quantidade", width=100)
tabela.column("minimo", width=110)
tabela.column("preco", width=100)

tabela.pack(fill="both", expand=True)

tabela.bind("<<TreeviewSelect>>", selecionar)


#Entrada e saída de produtos
movimento = tk.LabelFrame(
    tela,
    text="Entrada e saída de estoque",
    bg="#EEEEEE",
    padx=10,
    pady=10
)
movimento.pack(fill="x", padx=15, pady=10)

tk.Label(
    movimento,
    text="Selecione um produto na tabela e informe a quantidade:",
    bg="#EEEEEE"
).pack()

tk.Label(movimento, text="Quantidade:", bg="#EEEEEE").pack()

qtd_mov = tk.Entry(movimento)
qtd_mov.pack(pady=5)

tk.Button(
    movimento,
    text="Registrar entrada",
    command=lambda: movimentar("Entrada")
).pack(side="left", padx=10)

tk.Button(
    movimento,
    text="Registrar saída",
    command=lambda: movimentar("Saída")
).pack(side="left", padx=10)


#Mostrar produtos ao abrir o programa
listar()

tela.mainloop()
