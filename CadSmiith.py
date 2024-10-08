import customtkinter as ctk
from tkinter import messagebox, ttk, BOTH, END
import tkinter as tk
import sqlite3
import requests

# Configurações gerais para o tema dark
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Função para criar o banco de dados e a tabela de usuários
def criar_banco():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            data_nascimento TEXT NOT NULL,
            cep TEXT NOT NULL,
            endereco TEXT NOT NULL,
            quadra TEXT,
            lote TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Função para verificar o login do usuário
def verificar_login():
    if entry_usuario.get() == "admin" and entry_senha.get() == "admin":
        abrir_tela_cadastro()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorreto!")

def abrir_tela_cadastro():
    tela_login.destroy()
    tela_cadastro()

# Função para buscar o endereço via API de CEP
def buscar_endereco():
    cep = entry_cep_var.get().replace("-", "").strip()
    if len(cep) == 8:
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            dados = response.json()
            if 'erro' not in dados:
                entry_endereco_var.set(f"{dados['logradouro']}, {dados['bairro']}, {dados['localidade']}-{dados['uf']}")
            else:
                messagebox.showerror("Erro", "CEP não encontrado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar o CEP: {str(e)}")
    else:
        messagebox.showerror("Erro", "CEP inválido!")

def converter_para_maiusculas(*args):
    for var in lista_vars:
        var.set(var.get().upper())

def cadastrar_usuario():
    nome = entry_nome_var.get()
    cpf = entry_cpf_var.get()
    data_nascimento = entry_data_nascimento_var.get()
    cep = entry_cep_var.get()
    endereco = entry_endereco_var.get()
    quadra = entry_quadra_var.get()
    lote = entry_lote_var.get()

    if nome and cpf and data_nascimento and cep and endereco:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO usuarios (nome_completo, cpf, data_nascimento, cep, endereco, quadra, lote)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nome, cpf, data_nascimento, cep, endereco, quadra, lote))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            limpar_campos()
            entry_nome.focus()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Usuário já cadastrado com esse CPF!")
        finally:
            conn.close()
    else:
        messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos!")

def limpar_campos():
    entry_nome_var.set("")
    entry_cpf_var.set("")
    entry_data_nascimento_var.set("")
    entry_cep_var.set("")
    entry_endereco_var.set("")
    entry_quadra_var.set("")
    entry_lote_var.set("")
    entry_nome.focus()

def sair():
    tela_cadastro.destroy()

def ver_cadastros():
    tela_cadastro.withdraw()
    tela_lista_usuarios()

def voltar_para_cadastro():
    tela_lista.destroy()
    tela_cadastro.deiconify()

def editar_usuario(event):
    item = tree.focus()
    if item:
        valores = tree.item(item, 'values')
        abrir_tela_edicao(valores[0], valores[1])

def abrir_tela_edicao(nome, cpf):
    global entry_edicao_nome, entry_edicao_cpf, entry_edicao_data_nascimento, entry_edicao_cep, entry_edicao_endereco, entry_edicao_quadra, entry_edicao_lote, usuario_id

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome_completo=? AND cpf=?", (nome, cpf))
    usuario = cursor.fetchone()
    conn.close()

    usuario_id = usuario[0]

    tela_lista.withdraw()
    global tela_edicao
    tela_edicao = ctk.CTkToplevel()
    tela_edicao.title("Editar Usuário")
    tela_edicao.geometry("600x400")

    ctk.CTkLabel(tela_edicao, text="Nome Completo:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_edicao_nome = ctk.CTkEntry(tela_edicao, width=300)
    entry_edicao_nome.insert(0, usuario[1])
    entry_edicao_nome.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(tela_edicao, text="CPF:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_edicao_cpf = ctk.CTkEntry(tela_edicao, width=300)
    entry_edicao_cpf.insert(0, usuario[2])
    entry_edicao_cpf.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(tela_edicao, text="Data de Nascimento (dd/mm/yyyy):").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_edicao_data_nascimento = ctk.CTkEntry(tela_edicao, width=300)
    entry_edicao_data_nascimento.insert(0, usuario[3])
    entry_edicao_data_nascimento.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(tela_edicao, text="CEP:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_edicao_cep = ctk.CTkEntry(tela_edicao, width=150)
    entry_edicao_cep.insert(0, usuario[4])
    entry_edicao_cep.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(tela_edicao, text="Endereço:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
    entry_edicao_endereco = ctk.CTkEntry(tela_edicao, width=300)
    entry_edicao_endereco.insert(0, usuario[5])
    entry_edicao_endereco.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(tela_edicao, text="Quadra:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
    entry_edicao_quadra = ctk.CTkEntry(tela_edicao, width=300)
    entry_edicao_quadra.insert(0, usuario[6])
    entry_edicao_quadra.grid(row=5, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(tela_edicao, text="Lote:").grid(row=6, column=0, padx=10, pady=10, sticky="e")
    entry_edicao_lote = ctk.CTkEntry(tela_edicao, width=300)
    entry_edicao_lote.insert(0, usuario[7])
    entry_edicao_lote.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    frame_botoes_edicao = ctk.CTkFrame(tela_edicao)
    frame_botoes_edicao.grid(row=7, column=0, columnspan=2, pady=20)

    ctk.CTkButton(frame_botoes_edicao, text="Atualizar Cadastro", command=atualizar_usuario).pack(side=ctk.LEFT, padx=10)
    ctk.CTkButton(frame_botoes_edicao, text="Voltar", command=voltar_para_lista).pack(side=ctk.LEFT, padx=10)

def atualizar_usuario():
    nome = entry_edicao_nome.get()
    cpf = entry_edicao_cpf.get()
    data_nascimento = entry_edicao_data_nascimento.get()
    cep = entry_edicao_cep.get()
    endereco = entry_edicao_endereco.get()
    quadra = entry_edicao_quadra.get()
    lote = entry_edicao_lote.get()

    if nome and cpf and data_nascimento and cep and endereco:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE usuarios
                SET nome_completo=?, cpf=?, data_nascimento=?, cep=?, endereco=?, quadra=?, lote=?
                WHERE id=?
            ''', (nome, cpf, data_nascimento, cep, endereco, quadra, lote, usuario_id))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            tela_edicao.destroy()
            tela_lista_usuarios()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar o usuário: {str(e)}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos!")

def voltar_para_lista():
    tela_edicao.destroy()
    tela_lista.deiconify()

def excluir_usuario():
    item = tree.focus()
    if not item:
        messagebox.showerror("Erro", "Nenhum usuário selecionado!")
        return

    valores = tree.item(item, 'values')
    nome = valores[0]
    cpf = valores[1]

    resposta = messagebox.askyesno("Confirmação", f"Tem certeza de que deseja excluir o usuário {nome} (CPF: {cpf})?")
    if resposta:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE cpf = ?", (cpf,))
        conn.commit()
        conn.close()

        tree.delete(item)
        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")

def pesquisar_usuario():
    termo = entry_pesquisa.get().strip().upper()
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome_completo, cpf FROM usuarios WHERE nome_completo LIKE ? OR cpf LIKE ?", (f"%{termo}%", f"%{termo}%"))
    resultados = cursor.fetchall()

    for row in resultados:
        tree.insert("", tk.END, values=row)

    conn.close()

def tela_lista_usuarios():
    global tela_lista, tree, entry_pesquisa

    tela_lista = ctk.CTkToplevel()
    tela_lista.title("Lista de Usuários")
    tela_lista.geometry("650x450")

    ctk.CTkLabel(tela_lista, text="Pesquisar (Nome ou CPF):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_pesquisa = ctk.CTkEntry(tela_lista, width=200)
    entry_pesquisa.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    ctk.CTkButton(tela_lista, text="Pesquisar", command=pesquisar_usuario).grid(row=0, column=2, padx=10, pady=10)

    frame_tree = ctk.CTkFrame(tela_lista)
    frame_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    tree = ttk.Treeview(frame_tree, columns=("nome", "cpf"), show="headings")
    tree.heading("nome", text="Nome Completo")
    tree.heading("cpf", text="CPF")
    tree.pack(fill=BOTH, expand=True)

    tree.bind("<Double-1>", editar_usuario)

    # Carrega os dados dos usuários no TreeView
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome_completo, cpf FROM usuarios")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

    # Botões na parte inferior da tela
    frame_botoes_lista = ctk.CTkFrame(tela_lista)
    frame_botoes_lista.grid(row=2, column=0, columnspan=3, pady=10)

    ctk.CTkButton(frame_botoes_lista, text="Excluir Usuário", command=excluir_usuario).pack(side=ctk.LEFT, padx=10)
    ctk.CTkButton(frame_botoes_lista, text="Voltar", command=voltar_para_cadastro).pack(side=ctk.LEFT, padx=10)

def tela_login():
    global tela_login, entry_usuario, entry_senha

    tela_login = ctk.CTk()
    tela_login.title("Faça seu Login        |       Smiith Dev.")
    tela_login.geometry("450x360")

    

    ctk.CTkLabel(tela_login, text="Faça seu login", font=("Monaco", 30, "bold")).pack(pady=(25, 0))

    ctk.CTkLabel(tela_login, text="Usuário:", font=("Monaco", 14, "normal"), anchor="w").pack(pady=(35, 0), padx=125, fill="x")
    entry_usuario = ctk.CTkEntry(tela_login, width=200)
    entry_usuario.pack(pady=0)

    ctk.CTkLabel(tela_login, text="Senha:", font=("Monaco", 14, "normal"), anchor="w").pack(pady=(15, 0), padx=125, fill="x")
    entry_senha = ctk.CTkEntry(tela_login, show="*", width=200)
    entry_senha.pack(pady=0)

    ctk.CTkButton(tela_login, text="Entrar", command=verificar_login).pack(pady=25)

    texto = tk.Text(tela_login, height=0, width=27, font=("Arial", 12, "bold"),bd=0, bg="#2b2b2b", fg="#d6d6d6")
    texto.insert(tk.END, " Desenvolvido por ")
    texto.insert(tk.END, "SmiithDev.", "cor")  # Adicionando a tag 'cor' ao texto
    texto.insert(tk.END, " ® ")
    texto.tag_config("cor", foreground="#FF5733")  # Definindo a cor para 'SmiithDev'
    texto.config(state=tk.DISABLED)  # Desativar o widget para edição
    texto.pack(pady=(25, 0))

    #ctk.CTkLabel(tela_login, text="Desenvolvido por SmiithDev ® ").pack(pady=(10, 0))

    tela_login.mainloop()

def tela_cadastro():
    global tela_cadastro, entry_nome_var, entry_cpf_var, entry_data_nascimento_var, entry_cep_var, entry_endereco_var, entry_quadra_var, entry_lote_var
    global entry_nome, entry_cpf, entry_data_nascimento, entry_cep, entry_endereco, entry_quadra, entry_lote

    tela_cadastro = ctk.CTk()
    tela_cadastro.title("Cadastro de Usuário")
    tela_cadastro.geometry("650x400")

    entry_nome_var = ctk.StringVar()
    entry_cpf_var = ctk.StringVar()
    entry_data_nascimento_var = ctk.StringVar()
    entry_cep_var = ctk.StringVar()
    entry_endereco_var = ctk.StringVar()
    entry_quadra_var = ctk.StringVar()
    entry_lote_var = ctk.StringVar()

    global lista_vars
    lista_vars = [entry_nome_var, entry_cpf_var, entry_data_nascimento_var, entry_cep_var, entry_endereco_var, entry_quadra_var, entry_lote_var]

    for var in lista_vars:
        var.trace_add("write", converter_para_maiusculas)

    ctk.CTkLabel(tela_cadastro, text="Nome Completo:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_nome = ctk.CTkEntry(tela_cadastro, width=300, textvariable=entry_nome_var)
    entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    entry_nome.focus()

    ctk.CTkLabel(tela_cadastro, text="CPF:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_cpf = ctk.CTkEntry(tela_cadastro, width=300, textvariable=entry_cpf_var)
    entry_cpf.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(tela_cadastro, text="Data de Nascimento (dd/mm/yyyy):").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_data_nascimento = ctk.CTkEntry(tela_cadastro, width=300, textvariable=entry_data_nascimento_var)
    entry_data_nascimento.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(tela_cadastro, text="CEP:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_cep = ctk.CTkEntry(tela_cadastro, width=150, textvariable=entry_cep_var)
    entry_cep.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    entry_cep.bind("<FocusOut>", lambda event: buscar_endereco())

    ctk.CTkLabel(tela_cadastro, text="Endereço:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
    entry_endereco = ctk.CTkEntry(tela_cadastro, width=300, textvariable=entry_endereco_var)
    entry_endereco.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(tela_cadastro, text="Quadra:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
    entry_quadra = ctk.CTkEntry(tela_cadastro, width=300, textvariable=entry_quadra_var)
    entry_quadra.grid(row=5, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(tela_cadastro, text="Lote:").grid(row=6, column=0, padx=10, pady=10, sticky="e")
    entry_lote = ctk.CTkEntry(tela_cadastro, width=300, textvariable=entry_lote_var)
    entry_lote.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    frame_botoes = ctk.CTkFrame(tela_cadastro)
    frame_botoes.grid(row=7, column=0, columnspan=2, pady=20)

    ctk.CTkButton(frame_botoes, text="Cadastrar", command=cadastrar_usuario).pack(side=ctk.LEFT, padx=10)
    ctk.CTkButton(frame_botoes, text="Limpar", command=limpar_campos).pack(side=ctk.LEFT, padx=10)
    ctk.CTkButton(frame_botoes, text="Ver Cadastros", command=ver_cadastros).pack(side=ctk.LEFT, padx=10)
    ctk.CTkButton(frame_botoes, text="Sair", command=sair).pack(side=ctk.LEFT, padx=10)

    tela_cadastro.mainloop()

if __name__ == "__main__":
    criar_banco()
    tela_login()
