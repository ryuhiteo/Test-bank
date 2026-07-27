import pytest

from src.main.api.models.account_credit_repay_request import AccountCreditRepayRequest
from src.main.api.models.account_credit_request import AccountCreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.account_credit_repay_requester import AccountCreditRepayRequester
from src.main.api.requests.account_credit_requester import AccountCreditRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestAccountCreditRepay:
    # Тест на погашение кредита.
    def test_account_credit_repay_valid(self):
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

            account_id = response.id  # Дергаем ID нового счёта.

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

            # Запрос на погашение суммы кредита.
            account_credit_repay_request = AccountCreditRepayRequest(accountId=account_id, creditId=credit_id, amount=7500)

            response = AccountCreditRepayRequester(
                request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
                response_spec=ResponseSpecs.request_ok()
            ).post(account_credit_repay_request)

            response.creditId = credit_id
            response.amountDeposited = 7500


    # Негативные тесты на погашение кредита.
    @pytest.mark.parametrize(
        "username, password, amount",
        [
            # Входные данные для негативного теста.
            ("Rebeca", "Pas!sw0rd", 4500), # Кредит можно погасить только один раз, единовременно и на всю сумму.
        ]
    )
    def test_account_credit_repay_invalid(self, username, password, amount):
        # Создание нового юзера под админом.
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Запрос на создание счёта юзера.
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            response_spec=ResponseSpecs.request_created()
        ).post()

        account_id = response.id  # Дергаем ID нового счёта.

        # Запрос на получение кредита
        account_credit_request = AccountCreditRequest(accountId=account_id, amount=7500, termMonths=12)

        response = AccountCreditRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            response_spec=ResponseSpecs.request_created()
        ).post(account_credit_request)

        assert response.amount == 7500
        assert response.termMonths == 12
        assert response.balance == 7500

        credit_id = response.creditId

        # Запрос на погашение суммы кредита.
        account_credit_repay_request = AccountCreditRepayRequest(accountId=account_id, creditId=credit_id, amount=amount)

        response = AccountCreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            response_spec=ResponseSpecs.unprocessable_repayment() # Ловим ошибку 422
        ).post(account_credit_repay_request)




