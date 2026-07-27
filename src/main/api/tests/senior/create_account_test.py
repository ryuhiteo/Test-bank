import pytest

from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    # Тест для создания счёта.
    def test_create_account_valid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        # Запрос на создание счёта юзера.
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        account_from_db = Account.get_account_by_id(db_session, response.id)

        assert account_from_db.id == response.id, 'Ошибка: аккаунт не создан, id аккаунта нет в БД.'
        assert account_from_db.balance is not None, 'Ошибка: поле баланса для созданного аккаунта отсутствует в БД'



    # Негативный тест на создание счёта (пользователь уже имеет максимальное число счетов).
    def test_create_account_invalid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        # Первый счёт.
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        first_account_from_db = Account.get_account_by_id(db_session, response.id)

        assert first_account_from_db.id == response.id, 'Ошибка: аккаунт не создан, id аккаунта нет в БД.'
        assert first_account_from_db.balance is not None, 'Ошибка: поле баланса для созданного аккаунта отсутствует в БД'

        # Второй счёт.
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        second_account_from_db = Account.get_account_by_id(db_session, response.id)

        assert second_account_from_db.id == response.id, 'Ошибка: аккаунт не создан, id аккаунта нет в БД.'
        assert second_account_from_db.balance is not None, 'Ошибка: поле баланса для созданного аккаунта отсутствует в БД'

        # Третий счёт — превышение лимита.
        api_manager.user_steps.create_account_invalid(create_user_request)  # Ловим ошибку.



