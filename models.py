from database import db
import datetime

class Cliente(db.Model): # criação da classe Cliente
    id = db.Column(db.Integer, primary_key=True) #chave primária com auto incremento
    nome = db.Column(db.String(200))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(200))
    data_nascimento = db.Column(db.Date)
    ativo = db.Column(db.Boolean, default=True)

class EnvioMensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    data_envio = db.Column(db.DateTime, default=datetime.datetime.now)