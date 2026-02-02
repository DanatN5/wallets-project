from pydantic import BaseModel, Field
from enum import Enum


class Operation(str, Enum):
    withdraw = 'WITHDRAW'
    deposit = 'DEPOSIT'

class OperationTypeBase(BaseModel):
    type: Operation
    amount: int = Field(gt=0)