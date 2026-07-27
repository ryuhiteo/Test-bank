from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.account_credit_repay_request import AccountCreditRepayRequest
from src.main.api.models.account_credit_request import AccountCreditRequest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    # Создание счёта.
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
        RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
        Endpoint.CREATE_ACCOUNT,
        ResponseSpecs.request_created() # 201
        ).post()
        return response

    # Создание счёта сверх лимита (юзер уже имеет максимальное число счетов).
    def create_account_invalid(self, create_user_request: CreateUserRequest):
        response = CrudRequester(
        RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
        Endpoint.CREATE_ACCOUNT,
        ResponseSpecs.max_accounts_reached() # 409
        ).post()
        return response

    # Перевод средств между счетами.
    def transfer(self, create_user_request: CreateUserRequest, account_transfer_request: AccountTransferRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_TRANSFER,
            ResponseSpecs.request_ok() # 200
        ).post(account_transfer_request)
        return response

    # Перевод средств с невалидными данными.
    def transfer_invalid(self, create_user_request: CreateUserRequest, account_transfer_request: AccountTransferRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_TRANSFER,
            ResponseSpecs.request_bad() # 400
        ).post(account_transfer_request)
        return response

    # Пополнение счёта.
    def deposit(self, create_user_request: CreateUserRequest, account_deposit_request: AccountDepositRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_DEPOSIT,
            ResponseSpecs.request_ok() # 200
        ).post(account_deposit_request)
        return response

    # Пополнение счёта с невалидной суммой.
    def deposit_invalid(self, create_user_request: CreateUserRequest, account_deposit_request: AccountDepositRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_DEPOSIT,
            ResponseSpecs.request_bad() # 400
        ).post(account_deposit_request)
        return response

    # Получение кредита.
    def create_credit(self, create_user_request: CreateUserRequest, account_credit_request: AccountCreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created() # 201
        ).post(account_credit_request)
        return response

    # Получение кредита с невалидной суммой.
    def create_credit_invalid(self, create_user_request: CreateUserRequest, account_credit_request: AccountCreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_bad() # 400
        ).post(account_credit_request)
        return response

    # Получение кредита юзером без нужной роли.
    def create_credit_forbidden(self, create_user_request: CreateUserRequest, account_credit_request: AccountCreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_forbidden() # 403
        ).post(account_credit_request)
        return response

    # Погашение кредита.
    def repay_credit(self, create_user_request: CreateUserRequest, account_credit_repay_request: AccountCreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok() # 200
        ).post(account_credit_repay_request)
        return response

    # Погашение кредита частично (невалидное).
    def repay_credit_invalid(self, create_user_request: CreateUserRequest, account_credit_repay_request: AccountCreditRepayRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.unprocessable_repayment() # 422
        ).post(account_credit_repay_request)
        return response