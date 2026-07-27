from src.main.api.models.base_model import BaseModel


class AccountCreditRepayResponse(BaseModel):
        creditId: int
        amountDeposited: float