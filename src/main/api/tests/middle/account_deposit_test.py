import pytest

from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.account_deposit_requster import AccountDepositRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestAccountDeposit:
    # Тесты на переводы.
    def test_account_deposit_valid(self):
        # Создание нового юзера под админом.
        create_user_request = CreateUserRequest(username="Maximus", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Запрос на создание счёта юзера.
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        account_id = response.id # Дергаем ID нового счёта.

        # Делаем запрос на пополнение счёта.
        account_deposit_request = AccountDepositRequest(accountId=account_id, amount=9000)

        AccountDepositRequester(
            request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_deposit_request)


    # Негативные тесты на пополнение счёта.
    @pytest.mark.parametrize(
        "username, password, amount",
        [
            ("Albert", "Pas!sw0rd", 900 ), # Минимально 1000
            ("Shrek", "Pas!sw0rd", 10000) # Максимально 9000
        ]
    )
    def test_account_deposit_invalid(self, username, password, amount):
        # Создание нового юзера под админом.
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Запрос на создание счёта юзера.
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            response_spec=ResponseSpecs.request_created()
        ).post()

        account_id = response.id # Дергаем ID нового счёта.

        # Делаем запрос на пополнение счёта.
        account_deposit_request = AccountDepositRequest(accountId=account_id, amount=amount)

        AccountDepositRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            response_spec=ResponseSpecs.request_bad() # Ловим ошибку.
        ).post(account_deposit_request)

