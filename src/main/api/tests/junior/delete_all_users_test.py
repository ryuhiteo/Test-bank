import pytest
import requests


@pytest.mark.api
class TestDeleteAllUsers:
    def test_delete_all_users(self):
        # Авторизация под админом для получения токена
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


        # Запрос на удаление всех пользователей
        delete_all_users_response = requests.delete(
            url="http://localhost:4111/api/admin/users",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert delete_all_users_response.status_code == 200