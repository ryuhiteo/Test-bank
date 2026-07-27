import pytest

from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountTransfer:
    # Тест на перевод средств между счетами.
    def test_account_transfer_valid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_deposit_request: AccountDepositRequest, create_transfer_request: AccountTransferRequest):
        response = api_manager.user_steps.transfer(create_user_request, create_transfer_request)

        assert response.fromAccountIdBalance == create_deposit_request.balance - create_transfer_request.amount

        transaction_from_db = Transaction.get_transaction_by_to_account_id(db_session, create_transfer_request.toAccountId)

        assert transaction_from_db.to_account_id == create_transfer_request.toAccountId, 'Ошибка: транзакция не создана, id транзакции нет в БД.'
        assert transaction_from_db.amount == create_transfer_request.amount, 'Ошибка: amount БД не совпадает с amount ответа.'


    # Негативные тесты для перевода.
    @pytest.mark.parametrize(
        "amount",
        [
            400,  # Минимальный перевод 500
            11000,  # Максимальный перевод 10.000
        ]
    )
    def test_account_transfer_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, create_transfer_request: AccountTransferRequest, amount):
        create_transfer_request.amount = amount # Перезаписываем amount для негативного теста.
        api_manager.user_steps.transfer_invalid(create_user_request, create_transfer_request) # Ловим ошибку.




