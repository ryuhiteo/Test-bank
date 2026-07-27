from src.main.api.models.base_model import BaseModel


class AccountCreditRepayRequest(BaseModel):
    creditId: int
    accountId:  int
    amount: float