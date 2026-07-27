import pytest
import requests


@pytest.mark.api
class TestAccountDeposit:
    def test_account_deposit_valid(self):
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


        # Создание нового юзера.
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
        account_id = create_account_response.json().get("id")


        # Пополнение счёта.
        deposit_account_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": account_id,
                "amount": 1000
            },
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )

        assert deposit_account_response.status_code == 200


    @pytest.mark.parametrize(
        "username, amount, expected_status",
        [
            # Входные данные для негативного теста
            ("Maximus", 900, 400), # Минимально 1000
            ("Browny", 10000, 400), # Максимально 9000
        ]
    )

    def test_account_deposit_invalid(self, username, amount, expected_status):
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


        # Создание нового юзера.
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": username,
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
                "username": username,
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")


        # Запрос на создание счёта.
        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        account_id = create_account_response.json().get("id")


        # Пополнение счёта.
        deposit_account_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": account_id,
                "amount": amount
            },
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )

        assert deposit_account_response.status_code == expected_status