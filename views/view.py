import __init__
from models.model import Subscription, Payments
from models.database import engine
from sqlmodel import Session, select #Session cria uma seção de consulta na tabela e o select seleciona a tabela
from datetime import date, datetime

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
    
    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id) #Não a necessidade do join, pois esta consultando apenas 1 tabela
            result = session.exec(statement).one()
            session.delete(result)
            session.commit()
    
    def _has_pay(self, results): #Por padrão quando for uma função privada se inicia com um underline
        for result in results:
            if result.date.month == date.today().month:
                return True
        return False
    
    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Subscription.empresa==subscription.empresa)  #join serve para fazer uma intersecção entre duas tabelas
            results = session.exec(statement).all()                                                            #where é uma clausula de condição
                                                                                                              
            if self._has_pay(results):
                question = input("Essa conta já foi paga esse mês, deseja pagar novamente? Y ou N ")
                
                if not question.upper() == 'Y': #Upper serve para deixar as letras em maiusculo
                    return
                
            pay = Payments(subscription_id=subscription.id, date=date.today())
            session.add(pay)
            session.commit()
            print("Pagamento realizado com o sucesso!")
    
    def total_value(self):
        with Session(self.engine) as session:  
            statement = select(Subscription)
            results = session.exec(statement).all()
            
        total = 0
        for result in results:
            total+= result.valor
        
        return float(total)
    
    def  _get_last_12_months_native(self):
        today = datetime.now()
        year= today.year
        month = today.month
        last_12_month = []
        for _ in range (12): #Não a necessidade de uma variavel aqui entao se usa o _ como padrão
            last_12_month.append((month, year))
            month -= 1
            if month == 0:
                month = 12
                year -=1
        
        return last_12_month[::-1] #Se usa o [::-1] para mostrar o valor da antiga para a mais nova

    def _get_values_for_months(self, last_12_months):
        with Session(self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()
            
            value_for_months = []
            for i in last_12_months:
                value = 0
                for result in results:
                    if result.date.month == i[0] and result.date.year == i[1]:
                        value += float(result.subscription.valor)
                value_for_months.append(value)
            return value_for_months
    
    def gen_chart(self):
        last_12_months = self._get_last_12_months_native()
        values_for_months = self._get_values_for_months(last_12_months)
        
        last_12_months2 = []
        for i in last_12_months:
            last_12_months2.append(i[0])
          
        import matplotlib.pyplot as plt
        
        plt.plot(last_12_months2, values_for_months)
        plt.show()
                
ss = SubscriptionService(engine)


''' Exemplo de uso do enumerate:
assinaturas = ss.list_all()
for i, s in enumerate(assinaturas): #enumerate serve para usar uma variavel, no exemplo, i sem alterar o valor da varieavel s, como mostrado no exemplo
    print(f"[{i}] -> {s.empresa}")
    
x = int(input())

ss.pay(assinaturas[x])
'''