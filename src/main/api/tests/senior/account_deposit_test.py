import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestAccountDeposit:
    # Тест на пополнение счёта.
    def test_account_deposit_valid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        account = api_manager.user_steps.create_account(create_user_request)

        account_deposit_request = AccountDepositRequest(accountId=account.id, amount=9000)
        response = api_manager.user_steps.deposit(create_user_request, account_deposit_request)

        assert response.balance == 9000

        transaction_from_db = Transaction.get_transaction_by_to_account_id(db_session, account_deposit_request.accountId)

        assert transaction_from_db.to_account_id == account_deposit_request.accountId, 'Ошибка: транзакция не создана, id транзакции нет в БД.'
        assert transaction_from_db.amount == response.balance, 'Ошибка: amount БД не совпадает с amount ответа.'

    # Негативные тесты на пополнение счёта.
    @pytest.mark.parametrize(
        "amount",
        [
            900,    # Минимально 1000
            10000,  # Максимально 9000
        ]
    )
    def test_account_deposit_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, amount):
        account = api_manager.user_steps.create_account(create_user_request)

        account_deposit_request = AccountDepositRequest(accountId=account.id, amount=amount)
        api_manager.user_steps.deposit_invalid(create_user_request, account_deposit_request) # Ловим ошибку.