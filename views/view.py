import __init__
from models.model import Subscription
from models.database import engine
from sqlmodel import Session, select
from datetime import date

class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine
    
    def create(self, subscription: Subscription):
        with Session(self.engine) as session:
            session.add(subscription) #adiciona o arquivo
            session.commit() #salva o arquivo
            return subscription
    
    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
        return results
        
ss = SubscriptionService(engine)
#subscription = Subscription(empresa="netflix", site="netflix.com.br", data_assinatura=date.today(), valor=25)
print(ss.list_all())