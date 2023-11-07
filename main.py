from flask import Flask, render_template, request, make_response, request
from funcs import *
import json
from datetime import datetime

app = Flask(__name__)
app.static_url_path = '/static'
app.static_folder = 'static'


@app.route('/')
def index():
        nome_produto = request.args.get('nome_produto')
        descricao = request.args.get('descricao')
        categoria = request.args.get('categoria')
        marca = request.args.get('marca')
        preco_unitario = request.args.get('preco_unitario')
        quantidade = request.args.get('quantidade')
        import datetime
        data_cadastro = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dados_produto = (nome_produto, descricao, categoria, marca, preco_unitario, quantidade, data_cadastro)
        cadastro_produto(dados_produto)

        # Obtenha o HTML do menu suspenso
        custom_header = render_template('custom-header.html')
        
        # Renderize a página cadastro_produto.html e passe custom_header como variável de contexto
        return render_template('cadastro_produto.html', custom_header=custom_header)

@app.route('/login_CA', methods=['POST', 'GET'])
def login_user():
       
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']

        #Verificar se o login é válido
        e = login_user_valido(usuario, senha)

        if e:

            ck_usuario = {
            "usuario": usuario,
            "id_usuario": e[0][0]
            }
            json_texto = json.dumps(ck_usuario)
            
            res = make_response(render_template('main.html'))
            res.set_cookie( 
                key="usuario",
                value=json_texto,
                max_age= 600000, 
                #path = 
                domain=None,
                secure=False,
                httponly=False
                #samesite=False
            )
            return res
        else:
            #Criar alerta para login com erro
            error_message="Usuário ou senha incorreta"
            ck = get_cookies()
            image_url = "static/" + ck[0] + ".png"
            return render_template('login_CA.html', error=error_message, image_url=image_url)
    
    if request.method == 'GET':
        return verifica_login()

@app.route('/admin', methods=['POST', 'GET'])
def admin():

    if request.method == 'GET':
        print(request.form)    
        # Verifica se o campo oculto "tab" existe no formulário
        if 'tab' in request.form:
            aba_origem = request.form['tab']
            print(f"Pesquisa da aba: {aba_origem}")
            dados = [["1","2","3"],["4","5","6"]]
            return render_template('admin.html', dados=dados)
        else:
            return render_template('admin.html')
    
    if request.method == 'POST':
        print(request.form)    
        # Verifica se o campo oculto "tab" existe no formulário
        if 'tab' in request.form:
            #identifica de qual tab a informação está vindo
            aba_origem = request.form['tab']
            print(f"Formulário enviado da aba: {aba_origem}")
        return render_template('admin.html')

#EXEMPLO TESTE
@app.route('/teste', methods=['POST', 'GET'])
def testeexe():

    if request.method == 'GET':

        return render_template('cadastro_empresa.html')
    
    if request.method == 'POST':
       
        return 'ok'

if __name__ == '__main__':
    app.run()