import __init__
from models.model import Subscription, Payments
from models.database import engine
from sqlmodel import Session, select
from datetime import date

class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine
    
    def create(self, subscription: Subscription):
        with Session(self.engine) as session: #with é usado para finalizar um programa assim que o contexto do if e finalizado
            session.add(subscription) #adiciona o arquivo
            session.commit() #salva o arquivo
            return subscription
    
    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
        return results
    
    def _has_pay(seld, result):
        for result in results:
            if result.date.month == date.today(). month:#Por padrão quando for uma função privada se inicia com um underline
                return True
        return False
    
    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).where(Subscription.empresa==subscription.empresa)#where é uma clausula de condição
            results = session.exec(statement).all()
            pago = False
            for result in results:
                if result.date.month == date.today().month:
                    pago = True
            if pago:
                question = input("Essa conta jjá foi paga esse mês, deseja pagar novamente? Y ou N")
        
ss = SubscriptionService(engine)
subscription = Subscription(empresa="Netflix", site="netflix.com.br", data_assinatura=date.today(), valor=25)
ss.pay(subscription)