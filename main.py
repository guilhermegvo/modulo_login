from flask import Flask, render_template, request, make_response, request
from funcs import *
import json
import datetime

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
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
    
# GET = PEGAR VALORES | POST = CADASTRAR | PUT = ATUALIZAR | DELETE = DELETAR

#____________________________________________________________________________
#MAIN
@app.route('/main')
def index():
        # Renderize a página cadastro_produto.html e passe custom_header como variável de contexto
        return render_template('main.html')

#____________________________________________________________________________
#CADASTRO_CLIENTE
@app.route('/cadastro_cliente')
def cad_cliente():
    return render_template('cadastro_cliente.html')

@app.route('/api/cliente', methods=['POST', 'GET'])
def cliente():
    print(request)
    if request.method == 'POST':
        #data = request.get_json()
        nome_cliente = request.form['nome_cliente']
        cpf = request.form['cpf']
        email = request.form['email']
        cep = request.form['cep']
        endereco = request.form['endereco']
        cidade = request.form['cidade']
        estado = request.form['estado']
        telefone = request.form['telefone']
        
        dados_cliente = (nome_cliente, cpf, email, cep, endereco, cidade, estado, telefone)
        
        cadastro_cliente (dados_cliente)

        return render_template('cadastro_cliente.html')

#____________________________________________________________________________
#CADASTRO_EMPRESA
@app.route('/cadastro_empresa')
def cad_empresa():
        return render_template('cadastro_empresa.html')

@app.route('/api/empresa', methods=['POST', 'GET'])
def empresa():
    print(request)
    if request.method == 'POST':
        #data = request.get_json()
        nome_empresa = request.form['nome_empresa']
        cnpj = request.form['cnpj']
        email = request.form['email']
        cep = request.form['cep']
        endereco = request.form['endereco']
        cidade = request.form['cidade']
        estado = request.form['estado']
        telefone = request.form['telefone']
        
        dados_empresa = (nome_empresa, cnpj, email, cep, endereco, cidade, estado, telefone)
        
        cadastro_empresa(dados_empresa)

        return render_template('cadastro_empresa.html')

#____________________________________________________________________________
#CADASTRO_PRODUTO
@app.route('/cadastro_produto')
def cad_produto():
        # Renderize a página cadastro_produto.html e passe custom_header como variável de contexto
    return render_template('cadastro_produto.html')

@app.route('/api/produto', methods=['POST', 'GET'])
def produtos():
    print(request)
    if request.method == 'POST':
        #data = request.get_json()
        nome_produto = request.form['nome_produto']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        marca = request.form['marca']
        preco_unitario = request.form['preco_unitario']
        quantidade = request.form['quantidade']
        data_cadastro = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        dados_produto = (nome_produto, descricao, categoria, marca, preco_unitario, quantidade, data_cadastro)
        
        cadastro_produto(dados_produto)

        return render_template('cadastro_produto.html')

#____________________________________________________________________________
#CADASTRO_VENDA
@app.route('/cadastro_venda')
def cad_venda():
        return render_template('cadastro_venda.html')

@app.route('/api/venda', methods=['POST', 'GET'])
def venda():
    print(request)
    if request.method == 'POST':
        #data = request.get_json()
        produto = request.form['produto']
        descricao = request.form['descricao']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        cliente = request.form['cliente']
        data_cadastro = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        dados_venda = (produto, descricao, preco, quantidade, cliente, data_cadastro)
        
        cadastro_venda(dados_venda)

        return render_template('cadastro_venda.html')

#____________________________________________________________________________
#CONTAS_PAGAR
@app.route('/contas_pagar')
def con_pagar():
        # Renderize a página cadastro_produto.html e passe custom_header como variável de contexto
        return render_template('contas_pagar.html')

#____________________________________________________________________________
#CONTAS_RECBER
@app.route('/contas_receber')
def con_receber():
        # Renderize a página cadastro_produto.html e passe custom_header como variável de contexto
        return render_template('contas_receber.html')

#____________________________________________________________________________
#CONTROLE DE ESTOQUE   
# Rota para exibir a quantidade de produtos em estoque
@app.route('/controle_estoque')
def controle_estoque():
        produtos = get_lista_produtos()
        return render_template('controle_estoque.html', produtos=produtos)
    
if __name__ == '__main__':
    app.run()