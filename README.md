# modulo_login
 Um modulo de login utilizando flask no servidor

# ambiente virtual
 criar o ambiente na pasta raiz
    python -m venv venv
 ativar o ambiente virtual
    raiz/venv/Scripts/Activate.ps1

# atualizar ao salvar alterações
    no fim do arquivo raiz/main.py
        if __name__ == '__main__':
            app.run(debug=True)
    lembrar de alterar após o desenvolvimento

# bibliotecas
    Driver do Postgree
        pip install psycopg2
    Back end Flask
        pip install flask
    
