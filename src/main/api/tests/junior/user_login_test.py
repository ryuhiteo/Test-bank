import pytest
import requests


@pytest.mark.api
class TestUserLogin:
    def test_login_admin_valid(self):
        # Авторизация под админом
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        assert login_admin_response.json()["user"]["username"] == "admin"
        assert login_admin_response.json()["user"]["role"] == "ROLE_ADMIN"


    def test_login_user_valid(self):
        # Авторизация под админом, чтобы получить токен для создания юзера
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")


        # Создание юзера под правами админа.
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Maximus",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"

            }
        )

        assert create_user_response.status_code == 200


        # Авторизация под новыми данным юзера
        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Maximus",
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        assert login_user_response.json()["user"]["username"] == "Maximus"
        assert login_user_response.json()["user"]["role"] == "ROLE_USER"


    @pytest.mark.parametrize(
        "username, password",
        [
            # Входные данные для негативного теста авторизации юзера.
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
        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": username,
                "password": password
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        assert login_user_response.status_code == 401