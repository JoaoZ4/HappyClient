from database import db

class Cliente(db.Model): # criação da classe Cliente
    id = db.Column(db.Integer, primary_key=True) #chave primária com auto incremento
    nome = db.Column(db.String(200))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(200))
    data_nascimento = db.Column(db.Date)
    ativo = db.Column(db.Boolean, default=True)