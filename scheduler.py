from sqlalchemy import extract
from models import Cliente, EnvioMensagem
from app import app
from email.mime.text import MIMEText
from database import db
from dotenv import load_dotenv
import schedule, time, datetime, smtplib, os

load_dotenv()

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
                enviar_email(cliente.email, cliente.nome)
                envio = EnvioMensagem(cliente_id=cliente.id)
                db.session.add(envio)
                db.session.commit()
                print('Email enviado para: {}'.format(cliente.email))

schedule.every().day.at("08:00").do(verificar_aniversarios)
while True:
    schedule.run_pending()
    time.sleep(60)