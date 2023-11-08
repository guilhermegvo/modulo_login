from dbcon import PgConection
from flask import render_template, request, make_response
import json

PgCon = PgConection()

def get_cursor():
    conn = psycopg2.connect(
        host="silly.db.elephantsql.com",
        database="jrrgophc",
        user="jrrgophc",
        password="GlgXs8QFugqfKqkQ_lG9cV4ligNtq0mm"
    )
    return conn.cursor()



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




