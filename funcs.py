from dbcon import PgConection
from flask import render_template, request, make_response
import json
PgCon = PgConection()

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