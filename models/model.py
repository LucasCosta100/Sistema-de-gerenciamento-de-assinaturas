from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import date
from decimal import Decimal

class Subscription(SQLModel, table=True):#tabela criada para fazer o cadastramento das assinaturas
    id: int = Field(primary_key=True) #uma chave primaria, para o id nunca se repetir
    empresa: str
    site: Optional[str] = None
    data_assinatura: date
    valor: Decimal
    
class Payments(SQLModel, table=True):#tabela criada para saber se a assinatura ja foi paga
    id: int = Field(primary_key=True)
    subscription_id: int = Field(foreign_key="subscription.id")
    subscription: Subscription = Relationship()
    date: date
    