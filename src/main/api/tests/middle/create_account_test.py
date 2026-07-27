import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateAccount:
    # Тест для создания счёта.
    def test_create_account_valid(self):
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

            assert response.balance == 0


    # Негативный тест на создание счёта (пользователь уже имеет максимальное число аккаунтов).
    def test_create_account_invalid(self):
        # Создание нового юзера под админом.
        create_user_request = CreateUserRequest(username="Maximus", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Запрос на создание ПЕРВОГО счёта юзера.
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0

        # Запрос на создание ВТОРОГО счёта юзера.
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0

        # Запрос на создание ТРЕТЬЕГО счёта юзера.
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Maximus", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.max_accounts_reached() # Ловим ошибку.
        ).post()

