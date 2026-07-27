import pytest

from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    # Авторизация под админом.
    def test_login_admin_valid(self, api_manager):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    # Создание юзера и авторизация.
    def test_login_user_valid(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert  create_user_request.username == response.user.username
        assert  response.user.role == "ROLE_USER"


    # Негативный тест на авторизацию (STATUS = 401).
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
    def test_login_user_invalid(self, api_manager, username, password):
        login_user_request = LoginUserRequest(username=username, password=password)
        api_manager.admin_steps.login_user_invalid(login_user_request) # Ловим ошибку.
