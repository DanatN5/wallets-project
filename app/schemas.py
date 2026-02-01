from pydantic import BaseModel, Field
from enum import Enum


class AmountBase(BaseModel):
    amount: int = Field(gt=0)

class Operation(str, Enum):
    withdraw = 'WITHDRAW'
    deposit = 'DEPOSIT'

class OperationTypeBase(BaseModel):
    type: Operation

