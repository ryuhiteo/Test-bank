import pytest

from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.account_deposit_requster import AccountDepositRequester
from src.main.api.requests.account_transfer_requester import AccountTransferRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestAccountTransfer:
    # Тесты для перевода.
    def test_account_transfer_valid(self):
        # Создание ПЕРВОГО юзера под админом.
        create_user_request = CreateUserRequest(username="Maximus", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Создание ВТОРОГО юзера под админом.
        create_user_request = CreateUserRequest(username="Amogus", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Запрос на создание счёта ПЕРВОГО счёта user1.
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        user1_first_account_id = response.id # Первый счёт первого пользователя.

        # Делаем запрос на пополнение первого счёта user1.
        account_deposit_request = AccountDepositRequest(accountId=user1_first_account_id, amount=5000)

        response = AccountDepositRequester(
            request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_deposit_request)

        assert response.balance == 5000

        # Запрос на создание счёта ВТОРОГО счёта user1.
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        user1_second_account_id = response.id # Второй счёт первого пользователя.

        # Запрос на создание счёта ПЕРВОГО счёта user2.
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Amogus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        user2_first_account_id = response.id  # Первый счёт первого пользователя.

        # Запрос на перевод между счетами первого пользователя.
        account_transfer_request = AccountTransferRequest(fromAccountId=user1_first_account_id, toAccountId=user1_second_account_id, amount=5000)

        response = AccountTransferRequester(
            request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_transfer_request)

        assert response.fromAccountIdBalance == 0 # Проверяем, что после перевода баланс стал равен 0.

        # Запрос на перевод со ВТОРОГО счёта user1 на первый счёт user2.
        account_transfer_request = AccountTransferRequest(fromAccountId=user1_second_account_id, toAccountId=user2_first_account_id, amount=5000)

        response = AccountTransferRequester(
            request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_transfer_request)

        assert response.fromAccountIdBalance == 0 # Проверяем, что после перевода баланс стал равен 0.


    # Негативные тесты для перевода.
    @pytest.mark.parametrize(
        "username, password, amount",
        [
            # Входные данные для негативного теста.
            ("Boris", "Pas!sw0rd", 400), # Минимальный перевод 500
            ("Alice", "Pas!sw0rd", 11000), # Максимальный перевод 10000

        ]
    )
    def test_account_transfer_invalid(self, username, password, amount):
        # Создание юзера под админом.
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Запрос на создание счёта ПЕРВОГО счёта.
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        user1_first_account_id = response.id  # Первый счёт первого пользователя.

        # Запрос на пополнение первого счёта.
        account_deposit_request = AccountDepositRequest(accountId=user1_first_account_id, amount=5000)

        response = AccountDepositRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_deposit_request)

        assert response.balance == 5000

        # Ещё один запрос на пополнение первого счёта.
        account_deposit_request = AccountDepositRequest(accountId=user1_first_account_id, amount=9000)

        response = AccountDepositRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_deposit_request)

        assert response.balance == 14000

        # Запрос на создание счёта ВТОРОГО счёта.
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        user1_second_account_id = response.id  # Второй счёт первого пользователя.

        # Запрос на перевод между счетами первого пользователя.
        account_transfer_request = AccountTransferRequest(fromAccountId=user1_first_account_id, toAccountId=user1_second_account_id, amount=amount)

        response = AccountTransferRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            response_spec=ResponseSpecs.request_bad() # Ловим ошибку 420 (Не знаю почему 420, но логика такая. Баг?)
        ).post(account_transfer_request)




