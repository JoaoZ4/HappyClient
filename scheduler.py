from sqlalchemy import extract
from models import Cliente
from app import app
import schedule, time, datetime

def verificar_aniversarios():
    with app.app_context():
        clientes = Cliente.query.all()

        print("Verificando aniversários")
        aniversariantes = 'Os aniversariantes sao:'
        hoje = datetime.date.today()

        for cliente in clientes:
            if cliente.data_nascimento.day == hoje.day and cliente.data_nascimento.month == hoje.month:
                aniversariantes += f'\n{cliente.nome}'
        print(aniversariantes)

schedule.every().day.at("15:17").do(verificar_aniversarios)
while True:
    schedule.run_pending()
    time.sleep(60)