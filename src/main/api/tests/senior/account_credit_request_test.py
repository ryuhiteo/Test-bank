import pytest

from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.account_credit_request import AccountCreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit



@pytest.mark.api
class TestAccountCredit:
    # Тест на взятие кредита.
    def test_account_credit_request_valid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, create_credit_request: AccountCreditRequest):
        response = api_manager.user_steps.create_credit(create_credit_user_request, create_credit_request)

        assert response.amount == create_credit_request.amount
        assert response.termMonths == create_credit_request.termMonths
        assert response.balance == create_credit_request.amount

        credit_from_db = Credit.get_credit_by_to_account_id(db_session, create_credit_request.accountId)

        assert credit_from_db.amount == create_credit_request.amount, 'Ошибка: кредит не создан, amount кредита нет в БД.'
        assert credit_from_db.term_months == create_credit_request.termMonths, 'Ошибка: кредит не создан, termMonths кредита нет в БД.'

  # Негативные тесты на сумму кредита.
    @pytest.mark.parametrize(
        "amount",
        [
            450,    # Минимально 500
            16000,  # Максимально 10.000
        ]
    )
    def test_account_credit_request_invalid_amount(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, create_credit_request: AccountCreditRequest, amount):
        create_credit_request.amount = amount
        api_manager.user_steps.create_credit_invalid(create_credit_user_request, create_credit_request)

    # Негативный тест на проверку роли кредита.
    def test_account_credit_request_wrong_role(self, api_manager: ApiManager, create_user_request: CreateUserRequest, create_credit_request_wrong_role: CreateUserRequest):
        api_manager.user_steps.create_credit_forbidden(create_user_request, create_credit_request_wrong_role)