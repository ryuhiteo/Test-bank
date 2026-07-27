from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.requests.requester import Requester


class CreateAccountRequester(Requester):
    def post(self, model=None) -> CreateAccountResponse | Response:
        url=f"{self.base_url}/account/create"
        response = requests.post(
            url=url,
            headers=self.headers,
        )
        self.response_spec(response)

        # Проверка на положительный статус, чтобы после него возвращать ответ.
        if response.status_code == HTTPStatus.CREATED:
            return CreateAccountResponse(**response.json())
        return response