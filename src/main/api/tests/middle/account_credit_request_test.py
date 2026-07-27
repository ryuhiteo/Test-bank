import pytest

from src.main.api.models.account_credit_request import AccountCreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.account_credit_requester import AccountCreditRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestAccountCredit:
    # Тест на взятие кредита.
    def test_account_credit_request_valid(self):
        # Создание нового юзера под админом.
        create_user_request = CreateUserRequest(username="Maximus", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

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

        # Запрос на получение кредита
        account_credit_request = AccountCreditRequest(accountId=account_id, amount=7500, termMonths=12)

        response = AccountCreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(account_credit_request)

        assert response.amount == 7500
        assert response.termMonths == 12
        assert response.balance == 7500

        credit_id = response.creditId


    # Негативные тесты на взятие кредита.
    @pytest.mark.parametrize(
        "username, password, role, amount",
        [
            # Входные данные для негативного теста.
            ("Rebeca", "Pas!sw0rd", "ROLE_CREDIT_SECRET", 450), # Минимально 500
            ("Asteria", "Pas!sw0rd", "ROLE_CREDIT_SECRET", 16000), # Максимально 10000
            ("Aurelia", "Pas!sw0rd", "ROLE_USER", 12000) # ROLE_CREDIT_SECRET


        ]
    )
    def test_account_credit_request_invalid(self, username, password, role, amount):
        # Создание нового юзера под админом.
        create_user_request = CreateUserRequest(username=username, password=password, role=role)

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

        # Запрос на получение кредита
        if role == "ROLE_CREDIT_SECRET":
            account_credit_request = AccountCreditRequest(accountId=account_id, amount=amount, termMonths=12)

            response = AccountCreditRequester(
                request_spec=RequestSpecs.auth_headers(username=username, password=password),
                response_spec=ResponseSpecs.request_bad() # Ловим ошибку 400
            ).post(account_credit_request)
        else:
            account_credit_request = AccountCreditRequest(accountId=account_id, amount=amount, termMonths=12)

            response = AccountCreditRequester(
                request_spec=RequestSpecs.auth_headers(username=username, password=password),
                response_spec=ResponseSpecs.request_forbidden() # Ловим ошибку 403
            ).post(account_credit_request)




