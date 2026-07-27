import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestUserLogin:
    # Авторизация под админом.
    def test_login_admin_valid(self):
        login_user_request = LoginUserRequest(username="admin", password="123456")

        response = LoginUserRequester(
            request_spec=RequestSpecs.unauthentic_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    # Авторизация под юзером.
    def test_login_user_valid(self):
        # Создание юзера.
        create_user_request = CreateUserRequest(username="Maximus", password="Pas!sw0rd", role="ROLE_USER")

        response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        # Авторизация под новыми данным юзера.
        login_user_request = LoginUserRequest(username="Maximus", password="Pas!sw0rd")

        response = LoginUserRequester(
            request_spec=RequestSpecs.unauthentic_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_USER"


    # Негативный тест на авторизацию (STATUS=401).
    @pytest.mark.parametrize(
        "username, password",
        [
            # Входные данные для негативного теста.
            ("Борис", "Pas!sw0rd"),
            ("Vi", "Pas!sw0rd"),
            ("BorkusBorkusBorkus", "Pas!sw0rd"),
            ("Larison!", "Pas!sw0rd"),

            ("Viper", "Pas!sw0rdЫ"),
            ("Johny", "Pas!sw0"),
            ("Lepesh", "pas!sw0r"),
            ("Sasko", "PAS!SW0R"),
            ("Fresco", "Passw0rdd"),
            ("Gordon", "Passwordd"),
        ]
    )
    def test_login_user_invalid(self, username, password):
        login_user_request = LoginUserRequest(username=username, password=password)

        LoginUserRequester(
            request_spec=RequestSpecs.unauthentic_headers(),
            response_spec=ResponseSpecs.request_unauthorized()
        ).post(login_user_request)
