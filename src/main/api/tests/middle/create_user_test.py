import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateUser:
    # Тест на создание юзера.
    def test_create_user_valid(self):
        # Запрос на создание юзера.
        create_user_request = CreateUserRequest(username="Maximus", password="Pas!sw0rd", role="ROLE_USER")

        response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role


    # Негативный тест на создание юзера.
    @pytest.mark.parametrize(
        "username, password",
        [
            # Негативная проверка по логину
            ("Борис", "Pas!sw0rd"), # Только латиница
            ("Vi", "Pas!sw0rd"), # Минимум 3 символа
            ("BorkusBorkusBorkus", "Pas!sw0rd"), # Максимум 15 символов
            ("Larison!", "Pas!sw0rd"), # Запрещены спец.символы

            # Негативная проверка по паролю
            ("Viper", "Pas!sw0rdЫ"), # Только латиница
            ("Johny", "Pas!sw0"), # От 8-ми символов
            ("Lepesh", "pas!sw0r"), # Минимум 1 заглавная буква
            ("Sasko", "PAS!SW0R"), # Минимум 1 маленькая буква
            ("Fresco", "Passw0rdd"),  # Минимум 1 спец. символ
            ("Gordon", "Passwordd"), # Минимум 1 цифра
        ]
    )
    def test_create_user_invalid(self, username, password):
        # Запрос на создание пользователя
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_bad() # Ловим ошибку.
        ).post(create_user_request)
