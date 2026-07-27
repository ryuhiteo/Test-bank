import pytest
import requests


@pytest.mark.api
def login(username: str, password: str):
    # Функция авторизации. Возвращает токен.
    login_response = requests.post(
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

    assert login_response.status_code == 200
    return login_response.json().get("token") # Возвращаем токен авторизации.


def create_user(admin_token: str, username: str, password: str):
    # Функция создания пользователя под токеном админа.
    create_user_response = requests.post(
        url="http://localhost:4111/api/admin/create",
        json={
            "username": username,
            "password": password,
            "role": "ROLE_CREDIT_SECRET"
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {admin_token}"

        }
    )

    assert create_user_response.status_code == 200
    assert create_user_response.json().get("role") == "ROLE_CREDIT_SECRET"
    return create_user_response.json().get("role")


def create_user_account(user_token: str):
    # Создание счёта под токеном пользователя. Возвращаем ID счёта.
    create_user_account_response = requests.post(
        url="http://localhost:4111/api/account/create",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_token}"
        }
    )

    assert create_user_account_response.status_code == 201
    assert create_user_account_response.json().get("balance") == 0
    return create_user_account_response.json().get("id") # Возвращаем ID счёта


def credit_user_request(token: int, account_id: int, credit_user_amount: float, term_months: int):
    # Берем кредит на пользователя.
    credit_user_request_response = requests.post(
        url="http://localhost:4111/api/credit/request",
        json={
            "accountId": account_id,
            "amount": credit_user_amount,
            "termMonths": term_months
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )

    assert credit_user_request_response.status_code == 201
    assert credit_user_request_response.json().get("id") == account_id # Баг?
    assert credit_user_request_response.json().get("amount") == credit_user_amount
    assert credit_user_request_response.json().get("termMonths") == term_months
    return credit_user_request_response.json().get("creditId")


def credit_user_repay(token: str, account_id: int, credit_id: int, credit_repay_amount: float):
    # Погашение кредита пользователя.
    credit_user_repay_response = requests.post(
        url="http://localhost:4111/api/credit/repay",
        json={
            "creditId": credit_id,
            "accountId": account_id,
            "amount": credit_repay_amount
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )

    assert credit_user_repay_response.status_code == 200
    assert credit_user_repay_response.json().get("amountDeposited") == credit_repay_amount
    return credit_user_repay_response.json().get("creditId") # Возвращаем ID кредита


# Экспериментальный метод тестирования через функции.
def test_credit_valid():
    admin_token = login("admin", "123456")
    create_user(
        admin_token,
        username="pomni",
        password="Pas!sw0rd"
    )
    user_token = login("pomni", "Pas!sw0rd")
    user_account_id = create_user_account(user_token)
    user_credit_id = credit_user_request(
        user_token,
        user_account_id,
        5000,
        12
    )
    credit_user_repay(
        user_token,
        user_account_id,
        user_credit_id,
        5000
    )


# Негативные тесты на получение кредита.
@pytest.mark.parametrize(
        "username, password, credit_amount, term_months",
        [
            ("Johny", "Pas!sw0rd",  400, 12), # Минимально 1000
            ("Larisa", "Pas!sw0rd",  16000, 12), # Максимально 15000
        ]
    )

def test_credit_request_invalid(username, password, credit_amount, term_months):
    admin_token = login("admin", "123456")
    create_user(
        admin_token,
        username = username,
        password = password,
    )
    user_token = login(username=username, password=password)
    user_account_id = create_user_account(user_token)

    credit_user_request_response = requests.post(
        url="http://localhost:4111/api/credit/request",
        json={
            "accountId": user_account_id,
            "amount": credit_amount,
            "termMonths": term_months
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_token}"
        }
    )

    assert credit_user_request_response.status_code == 400 # Ловим ошибку.