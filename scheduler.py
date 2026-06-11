from sqlalchemy import extract
from models import Cliente, EnvioMensagem
from app import app
from email.mime.text import MIMEText
from database import db
from dotenv import load_dotenv
import schedule, time, datetime, smtplib, os
import requests

load_dotenv()

def enviar_mensagem(telefone, nome):
    phoneId = os.environ.get('ID_PHONE_NUMBER')
    token = os.environ.get('TOKEN_META')
    url = f'https://graph.facebook.com/v25.0/{phoneId}/messages'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    body = {
        "messaging_product": "whatsapp",
        "to": f"{telefone}",
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": { "code": "en_US" }
        }
    }

    resposta = requests.post(url, headers=headers, json=body)
    print(resposta.json())

def enviar_email(destinatario, nome):
    remetente = os.environ.get('EMAIL_REMETENTE')
    senha = os.environ.get('EMAIL_SENHA')
    mensagem = MIMEText(f'Feliz aniversário {nome}')
    mensagem['Subject'] = 'Feliz Aniversário!'
    mensagem['From'] = remetente
    mensagem['To'] = destinatario

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha)
        smtp.sendmail(remetente, destinatario, mensagem.as_string())

def verificar_aniversarios():
    with app.app_context():
        clientes = Cliente.query.all()
        hoje = datetime.date.today()

        for cliente in clientes:
            if cliente.data_nascimento.day == hoje.day and cliente.data_nascimento.month == hoje.month:
                tel_formatado = '55' + cliente.telefone
                enviar_email(cliente.email, cliente.nome)
                enviar_mensagem(tel_formatado, cliente.nome)
                envio = EnvioMensagem(cliente_id=cliente.id)
                db.session.add(envio)
                db.session.commit()
                print('Email enviado para: {}\nMensagem enviada para: {}'.format(cliente.email, tel_formatado))

schedule.every().day.at("08:00").do(verificar_aniversarios)
while True:
    schedule.run_pending()
    time.sleep(60)