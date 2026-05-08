from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, ConfigDict, condecimal


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class OperationRequest(BaseModel):
    operation_type: OperationType
    amount: condecimal(gt=0, max_digits=10, decimal_places=2)


class WalletResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    wallet_id: str
    balance: Decimal