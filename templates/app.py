import __init__
from views.view import SubscriptionService
from models.database import engine
from models.model import Subscription
from datetime import datetime
from decimal import Decimal

class UI:
    def __init__(self):
        self.subscription_service = SubscriptionService(engine)
    
    def start(self):
        while True:
            print('''            ==================================
            |       MENU DE ASSINATURAS      |
            ==================================
            |                                |''')
            print('''            | [1] -> Adicionar assinatura    |
            | [2] -> Remover assinatura      |
            | [3] -> Valor total             |
            | [4] -> Gastos últimos 12 meses |
            | [5] -> Status pagamentos       |
            | [6] -> Sair                    |
            |                                |''')
            print("            ==================================")
            choice = int(input('Escolha uma opção: '))

            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.delete_subscription()
            elif choice == 3:
                self.total_value()
            elif choice == 4:
                self.subscription_service.gen_chart()
            elif choice == 5:
                self.pay_subscription()
            else:
                break

    def add_subscription(self):
        empresa = input("Empresa: ")
        site = input("Site: ")
        data_assinatura = datetime.strptime(input("Data de assinatura: "), "%d/%m/%Y")
        valor: Decimal = (input("Valor: "))
        subscription = Subscription(empresa=empresa, site=site, data_assinatura=data_assinatura, valor=valor)
        self.subscription_service.create(subscription)
        
    def delete_subscription(self):
        subscriptions = self.subscription_service.list_all()
        #extra: Quando excluir a assinatura, excluir todos os pagamentos dela.
        print("Escolha qual assinatura deseja excluir")
        
        for i in subscriptions:
            print(f"[{i.id}] -> {i.empresa}")
        
        choice = int(input("Escolha a assinatura: "))
        self.subscription_service.delete(choice)
        print("Assinatura excluida com secusso!")

    def total_value (self):
        subscriptions = self.subscription_service.list_all()
        print("___________________________________________________") 
        for i in subscriptions:
            print (f"[{i.id}]  {i.empresa} - \t{i.valor:.2f} ")
            
        print("___________________________________________________")     
        print(f"Seu valor total mensal em assinatura é: {self.subscription_service.total_value()}")
        print("___________________________________________________") 
        
    #def pay_subscription(self):
        
if __name__ == '__main__':
    UI().start()  