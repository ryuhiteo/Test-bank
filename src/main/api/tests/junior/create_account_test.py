import pytest
import requests


@pytest.mark.api
class TestCreateAccount:
    def test_create_account_valid(self):
            # Авторизация под админом.
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


            # Создание нового юзера под админом.
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


            # Авторизация под новыми данными юзера.
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
            token = login_user_response.json().get("token")


            # Запрос на создание счёта юзера.
            create_account_response = requests.post(
                url="http://localhost:4111/api/account/create",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )

            assert create_account_response.status_code == 201
            assert create_account_response.json().get("balance") == 0


    def test_create_account_invalid(self):
        # Авторизация под админом.
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


        # Создание нового юзера под админом.
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


        # Авторизация под новыми данным юзера.
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
        token = login_user_response.json().get("token")


        # Запрос на создание ПЕРВОГО счёта с аккаунта юзера.
        create_first_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        # Запрос на создание ВТОРОГО счёта с аккаунта юзера.
        create_second_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        # Запрос на создание ТРЕТЬЕГО счёта с аккаунта юзера (негативный тест).
        create_third_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_first_account_response.status_code == 201
        assert create_second_account_response.status_code == 201
        assert create_third_account_response.status_code == 409 # Ловим ошибку.