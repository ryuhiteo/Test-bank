import pytest

from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.account_credit_repay_request import AccountCreditRepayRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit



@pytest.mark.api
class TestAccountCreditRepay:
    # Тест на погашение кредита.
    def test_account_credit_repay_valid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request : CreateUserRequest, create_credit_repay_request: AccountCreditRepayRequest):
        response = api_manager.user_steps.repay_credit(create_credit_user_request, create_credit_repay_request)

        assert response.creditId == create_credit_repay_request.creditId
        assert response.amountDeposited == create_credit_repay_request.amount

        credit_from_db = Credit.get_credit_by_to_account_id(db_session, create_credit_repay_request.accountId)

        assert credit_from_db.account_id == create_credit_repay_request.accountId, 'Ошибка: кредит не создан, id кредита нет в БД.'
        assert credit_from_db.amount == create_credit_repay_request.amount, 'Ошибка: кредит не создан, amount кредита нет в БД.'

    # Негативный тест — кредит можно погасить только один раз, единовременно и на всю сумму.
    def test_account_credit_repay_invalid_partial(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, create_credit_repay_request: AccountCreditRepayRequest):
        create_credit_repay_request.amount = 4500  # Пытаемся погасить неполную сумму, вместо 7500.
        api_manager.user_steps.repay_credit_invalid(create_credit_user_request, create_credit_repay_request) # Ловим ошибку.




