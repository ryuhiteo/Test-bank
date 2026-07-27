import pytest

from src.main.api.requests.delete_all_user_requester import DeleteAllUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestDeleteAllUsers:
    # Удаление всех пользователей.
    def test_delete_all_users(self):
        # Запрос на удаление всех пользователей
        DeleteAllUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post()


