import pytest
import requests


@pytest.mark.api
class TestAccountTransfer:
    def test_account_transfer_valid(self):
        #Авторизация под админом.
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


    # Создание первого юзера.
        create_user1_response = requests.post(
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

        assert create_user1_response.status_code == 200


    # Создание второго юзера.
        create_user2_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Goofy",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"

            }
        )

        assert create_user2_response.status_code == 200


    # Авторизация под новыми данным первого юзера.
        login_user1_response = requests.post(
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

        assert login_user1_response.status_code == 200
        token_user1 = login_user1_response.json().get("token")


    # Запрос на создание счёта через первого юзера.
        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_user1}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        first_account_id_user1 = create_account_response.json().get("id")


        # Запрос на создание второго счёта через первого юзера.
        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_user1}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        second_account_id_user1 = create_account_response.json().get("id")


    # Пополнение первого счёта первого юзера.
        deposit_account_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": first_account_id_user1,
                "amount": 2000
            },
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token_user1}",
                "Content-Type": "application/json",
            }
        )

        assert deposit_account_response.status_code == 200


    # Авторизация под новыми данным второго юзера.
        login_user2_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Goofy",
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        assert login_user2_response.status_code == 200
        token_user2 = login_user2_response.json().get("token")


    # Запрос на создание счёта с аккаунта второго юзера.
        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_user2}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        account_id_user2 = create_account_response.json().get("id")


    # Пополнение счёта второго юзера.
        deposit_account_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": account_id_user2,
                "amount": 1500
            },
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token_user2}",
                "Content-Type": "application/json",
            }
        )

        assert deposit_account_response.status_code == 200


        # Перевод: first_account_id_user1 на first_account_id_user2
        transfer_account_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": first_account_id_user1,
                "toAccountId": second_account_id_user1,
                "amount": 500
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "authorization": f"Bearer {token_user1}"
            }
        )

        assert transfer_account_response.status_code == 200
        assert transfer_account_response.json()["fromAccountId"] == first_account_id_user1
        assert transfer_account_response.json()["toAccountId"] == second_account_id_user1
        assert transfer_account_response.json()["fromAccountIdBalance"] == 1500


    # Запрос на перевод: user2 на second_account_id_user1.
        transfer_account_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": account_id_user2,
                "toAccountId": second_account_id_user1,
                "amount": 500
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "authorization": f"Bearer {token_user2}"
            }
        )

        assert transfer_account_response.status_code == 200
        assert transfer_account_response.json()["fromAccountId"] == account_id_user2
        assert transfer_account_response.json()["toAccountId"] == second_account_id_user1
        assert transfer_account_response.json()["fromAccountIdBalance"] == 1000


    # Негативный тест на перевод.
    def test_account_transfer_invalid(self):
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


        # Создание первого юзера.
        create_user1_response = requests.post(
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

        assert create_user1_response.status_code == 200


        # Создание второго юзера.
        create_user2_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Goofy",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"

            }
        )

        assert create_user2_response.status_code == 200


        # Авторизация под новыми данным первого юзера.
        login_user1_response = requests.post(
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

        assert login_user1_response.status_code == 200
        token_user1 = login_user1_response.json().get("token")


        # Запрос на создание счёта первого юзера.
        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_user1}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        account_id_user1 = create_account_response.json().get("id")


        # Пополнение счёта первого юзера.
        deposit_account_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": account_id_user1,
                "amount": 1000
            },
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token_user1}",
                "Content-Type": "application/json",
            }
        )

        assert deposit_account_response.status_code == 200


        # Авторизация под новыми данным второго юзера.
        login_user2_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Goofy",
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        assert login_user2_response.status_code == 200
        token_user2 = login_user2_response.json().get("token")


        # Запрос на создание счёта с аккаунта второго юзера.
        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_user2}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        account_id_user2 = create_account_response.json().get("id")


        # Пополнение счёта второго юзера.
        deposit_account_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": account_id_user2,
                "amount": 1500
            },
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token_user2}",
                "Content-Type": "application/json",
            }
        )

        assert deposit_account_response.status_code == 200


        # Запрос на перевод: user2 на user1 (Негативный: перевод < 500)
        transfer_account_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": account_id_user2,
                "toAccountId": account_id_user1,
                "amount": 0
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "authorization": f"Bearer {token_user2}"
            }
        )

        assert transfer_account_response.status_code == 400 # Ловим ошибку