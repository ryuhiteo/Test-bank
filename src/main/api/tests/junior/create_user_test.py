import pytest
import requests


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self):
        # Авторизация под админом, чтобы создать пользователя.
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


        # Запрос на создание пользователя.
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
        assert create_user_response.json().get("username") == "Maximus"
        assert create_user_response.json().get("role") == "ROLE_USER"


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
        # Авторизация под админом, чтобы создать пользователя
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

        token = login_admin_response.json().get("token")


        # Запрос на создание пользователя
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": username,
                "password": password,
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"

            }
        )

        assert create_user_response.status_code == 400