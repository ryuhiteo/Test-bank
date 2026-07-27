from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.account_transfer_response import AccountTransferResponse
from src.main.api.requests.requester import Requester


class AccountTransferRequester(Requester):
    def post(self, account_transfer_request: AccountTransferRequest) -> AccountTransferResponse | Response:
        url=f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=account_transfer_request.model_dump(),
            headers=self.headers,
        )
        self.response_spec(response)

        # Проверка на положительный статус, чтобы после него возвращать ответ.
        if response.status_code in [HTTPStatus.OK]:
            return AccountTransferResponse(**response.json())
        return response
