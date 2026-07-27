from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.delete_all_user_response import DeleteAllUsersResponse
from src.main.api.requests.requester import Requester


class DeleteAllUserRequester(Requester):
    def post(self, model=None) -> DeleteAllUsersResponse | Response:
        url=f"{self.base_url}/admin/users"
        response = requests.delete(
            url=url,
            headers=self.headers,
        )
        self.response_spec(response)

        # Проверка на положительный статус, чтобы после него возвращать ответ.
        if response.status_code in [HTTPStatus.OK]:
            return DeleteAllUsersResponse(**response.json())
        return response