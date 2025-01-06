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
    
    def _has_pay(self, results): #Por padrão quando for uma função privada se inicia com um underline
        for result in results:
            if result.date.month == date.today(). month:
                return True
        return False
    
    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Subscription.empresa==subscription.empresa) #where é uma clausula de condição 
            results = session.exec(statement).all()                                                           #join serve para fazer uma intersecção entre duas tabelas
            
            if self._has_pay(results):
                question = input("Essa conta já foi paga esse mês, deseja pagar novamente? Y ou N")
                
                if not question.upper() == 'Y': #Upper serve para deixar as letras em maiusculo
                    return
                
            pay = Payments(subscription_id=subscription.id, date=date.today())
            session.add(pay)
            session.commit()
                
        
ss = SubscriptionService(engine)

assinaturas = ss.list_all()
for i, s in enumerate(assinaturas):
    print(f"[{i}] -> {s.empresa}")
    
x = int(input())

ss.pay(assinaturas[x])