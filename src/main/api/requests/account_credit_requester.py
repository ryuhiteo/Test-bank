from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.account_credit_request import AccountCreditRequest
from src.main.api.models.account_credit_response import AccountCreditResponse
from src.main.api.requests.requester import Requester


class AccountCreditRequester(Requester):
    def post(self, account_credit_request: AccountCreditRequest) -> AccountCreditResponse | Response:
        url=f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            json=account_credit_request.model_dump(),
            headers=self.headers,
        )
        self.response_spec(response)

        # Проверка на положительный статус, чтобы после него возвращать ответ.
        if response.status_code in [HTTPStatus.CREATED]:
            return AccountCreditResponse(**response.json())
        return response