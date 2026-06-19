from flask import Flask, render_template, request, redirect, session # classe de inicialização do flask
from database import db # import da conexão do banco
from sqlalchemy import or_ # para usar o filter com o método 'ou'
import os # módulo para manipular o file system
from models import Cliente, EnvioMensagem # objeto a ser criado no banco
import datetime

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# __file__ é o caminho do próprio app.py
# os.path.dirname pega a pasta onde ele esta
# os.path.abspath transforma em caminho absoluto completo

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'happyclient.db')
# o join monta o caminho final onde o app ira se conectar
db.init_app(app)

with app.app_context():
    db.create_all() # diz para o banco que pode criar as tabelas no contexto desse app

app.secret_key = 'happyclient123'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['usuario'] == 'admin' and request.form['senha'] == '1234':
            session['logado'] = True
            return redirect('/')
        else:
            return redirect('/login')
    else:
        return render_template('login.html')

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST']) # rota para editar registros
def editar(id):
    if not session.get('logado'):
        return redirect('/login')
    else:
        if request.method == 'GET':
            cliente = Cliente.query.get(id) # busca no banco o cliente que quer editar
            return render_template('editar.html', cliente=cliente) # passa como parametro para o template editar.html
                                                                # que ira carregar os campos pré definidos com os dados do cliente
        else:
            cliente = Cliente.query.get(id) # coleta o cliente
            cliente.nome = request.form['nome'] # atualiza com os novos valores
            cliente.telefone = request.form['telefone']
            cliente.email = request.form['email']
            nasc = request.form['data_nascimento']
            cliente.data_nascimento = datetime.datetime.strptime(nasc, '%Y-%m-%d').date()
            db.session.commit() # publica no banco de dados
            return redirect('/clientes') # e volta para a main
        

@app.route('/clientes/excluir/<int:id>') # rota para excluir um registro
def excluir(id):
    if not session.get('logado'):
        return redirect('/login')
    else:
        cliente = Cliente.query.get(id) # coleta o objeto
        db.session.delete(cliente) # deleta
        db.session.commit() # publica
        return redirect('/clientes') # volta para a main

@app.route('/clientes/cadastrar', methods=['POST']) # rota para realizar o cadastro de clientes
def cadastrar():
    if not session.get('logado'):
        return redirect('/login')
    else:
        nome = request.form['nome'] # coleta os dados recebidos pelo formulário
        telefone = request.form['telefone']
        email = request.form['email']
        data_nascimento = request.form['data_nascimento']
        data_nascimento = datetime.datetime.strptime(data_nascimento, '%Y-%m-%d').date() # conversão da data, de string 
                                                                                        # para um objeto date em python
        cliente = Cliente(nome=nome, telefone=telefone, email=email, data_nascimento=data_nascimento) # instanciando o objeto Cliente
        db.session.add(cliente) # adicionando ao banco
        db.session.commit() # publicando ao banco
        return redirect('/clientes')

@app.route('/clientes', methods=['GET'])
def clientes():
    if not session.get('logado'):
        return redirect('/login')
    else:
        busca = request.args.get('busca', '') # coletar o input da busca
        if busca == '': # se nao foi digitado nada
            clientes = Cliente.query.all() # coleta todos os registros do banco
        else:
            clientes = Cliente.query.filter( # sintaxe do filtro
                or_(
                    Cliente.nome.like(f'%{busca}%'),
                    Cliente.email.like(f'%{busca}%'), # Pesquisa no campo nome ou email ou telefone pelo que foi inserido no campo busca
                    Cliente.telefone.like(f'%{busca}%')
                )
            ).all() # e pega todos os registros encontrados
        return render_template('clientes.html', clientes=clientes) # retorna renderizando a tela clientes.html 
                                                               # passando a lista de clientes resultante

@app.route('/') # configuração da rota principal
def index():
    if not session.get('logado'):
        return redirect('/login')
    else:
        hoje = datetime.date.today()
        daqui_7_dias = hoje + datetime.timedelta(days=7)
        niver_hoje = 0
        niver_semana = 0
        tot_clientes = Cliente.query.count()
        clientes = Cliente.query.all()
        total_mensagens = EnvioMensagem.query.count()

        for cliente in clientes:
            niver_ano_atual = cliente.data_nascimento.replace(year = hoje.year)
            if hoje < niver_ano_atual <= daqui_7_dias:
                niver_semana += 1
            if cliente.data_nascimento.month == hoje.month and cliente.data_nascimento.day == hoje.day:
                niver_hoje += 1

        return render_template('dashboard.html', 
                               tot_clientes=tot_clientes, 
                               niver_hoje=niver_hoje, 
                               niver_semana=niver_semana, 
                               total_mensagens=total_mensagens) # retorna renderizando a tela dashboard.html, passando os dados que precisamos para o front

if __name__ == '__main__':
    app.run(debug=True) # inicia o servidor local