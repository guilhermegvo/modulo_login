from dbcon import PgConection
from flask import render_template, request, make_response
import json

PgCon = PgConection()

def get_cursor():
    try:
        conn = psycopg2.connect(
            host="silly.db.elephantsql.com",
            database="jrrgophc",
            user="jrrgophc",
            password="GlgXs8QFugqfKqkQ_lG9cV4ligNtq0mm"
        )
        return conn.cursor()
    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

def login_user_valido(usuario, senha):
    PgCon = PgConection()
    query = "SELECT id_usuario FROM usuarios WHERE usuario = '%s' AND senha = '%s'" % (usuario, senha)
    id = PgCon.executar_query(query)
    PgCon.desconectar()
 
    return id
    
def login_empresa_valido(empresa, senha):
    PgCon = PgConection()
    #Cirar tabela empresa com FK na tabela usuarios
    query = "SELECT id_empresa FROM empresas WHERE empresa = '%s' AND senha = '%s'" % (empresa, senha)
    id = PgCon.executar_query(query)
    PgCon.desconectar()

    return id

def get_cookies():
    cookies =  request.cookies
    ck_empresa = cookies.get("empresa")
    res = []
    if ck_empresa:
        empresa = json.loads(ck_empresa)
        ck_user = cookies.get("usuario")
        if ck_user:
            user = json.loads(ck_user)
            res = [empresa["empresa"], empresa["id_empresa"], user["usuario"], user["id_usuario"]]
        else:
            res = [empresa["empresa"], empresa["id_empresa"]]
    #retorno: [empresa, id_empresa, usuario, id_usuario]
    return res

def verifica_login():

    ck = get_cookies()

    if len(ck)>0:
    
        if len(ck)>2:
            res = make_response(render_template('main.html'))
            return res        
        else:
            #print("Usuario não logado!")
            image_url = "static/" + ck[0] + ".png"
            res = make_response(render_template('login_user.html', image_url=image_url))
            return res
    else:
        #print("Empresa não logado!")
        res = make_response(render_template('login_CA.html'))
        return res
    

#Inserir os dados em cadastro_produto

#INSERT INTO clientes (nome_cliente, cpf, email, cep, endereco, cidade, estado, telefone, data_cadastro) VALUES
#   ('Cliente 1', '123.456.789-01', 'cliente1@email.com', '12345-678', 'Rua A, 123', 'Cidade A', 'Estado A', '(123) 456-7890', '2023-11-05'),

import psycopg2

#____________________________________________________________________________
#CADASTRO_CLIENTE
def cadastro_cliente(dados_cliente):
    conn = None
    try:
        cursor = get_cursor()
        query = """
            INSERT INTO cadastro_produto (nome_cliente, cpf, email, cep, endereco, cidade, estado, telefone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, dados_cliente)
        id = cursor.fetchone()[0]
        conn.commit()
        return id
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro: {error}")
    finally:
        if conn is not None:
            conn.close()

#____________________________________________________________________________
#CADASTRO_EMPRESA
def cadastro_empresa(dados_empresa):
    conn = None
    try:
        cursor = get_cursor()
        query = """
            INSERT INTO cadastro_produto (nome_empresa, cnpj, email, cep, endereco, cidade, estado, telefone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, dados_empresa)
        id = cursor.fetchone()[0]
        conn.commit()
        return id
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro: {error}")
    finally:
        if conn is not None:
            conn.close()

#____________________________________________________________________________
#CADASTRO_PRODUTO
def cadastro_produto(dados_produto):
    conn = None
    try:
        cursor = get_cursor()
        query = """
            INSERT INTO cadastro_produto (nome_produto, descricao, categoria, marca, preco_unitario, quantidade, data_cadastro)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, dados_produto)
        id = cursor.fetchone()[0]
        conn.commit()
        return id
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro: {error}")
    finally:
        if conn is not None:
            conn.close()

#____________________________________________________________________________
#CADASTRO_VENDAS
def cadastro_venda(dados_venda):
    conn = None
    try:
        cursor = get_cursor()
        query = """
            INSERT INTO cadastro_produto (produto, descricao, preco, quantidade, cliente, data_cadastro)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, dados_venda)
        id = cursor.fetchone()[0]
        conn.commit()
        return id
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro: {error}")
    finally:
        if conn is not None:
            conn.close()
    
#____________________________________________________________________________
#CONTROLE_ESTOQUE           
# Função para obter a quantidade de produtos em estoque
def get_lista_produtos():
    conn = get_cursor()

    if conn:
        try:
            cursor = conn

            # Consulta para obter a lista de produtos
            query = "SELECT * FROM cadastro_produto"
            cursor.execute(query)

            lista_produtos = cursor.fetchall()

            return lista_produtos
        except psycopg2.Error as e:
            print("Erro ao executar a consulta:", e)
            return []
        finally:
            conn.close()
    else:
        return []