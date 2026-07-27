import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_credit_repay_request import AccountCreditRepayRequest
from src.main.api.models.account_credit_request import AccountCreditRequest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.create_user_request import CreateUserRequest


# Создание случайного юзера с ролью ROLE_USER.
@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

# Создание счёта для юзера.
@pytest.fixture
def create_account(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)

# Пополнение счёта на 9000.
@pytest.fixture
def create_deposit_request(api_manager, create_user_request, create_account):
    deposit_request = AccountDepositRequest(accountId=create_account.id, amount=9000)
    response = api_manager.user_steps.deposit(create_user_request, deposit_request)
    return response

# Запрос на перевод.
@pytest.fixture
def create_transfer_request(api_manager, create_user_request, create_deposit_request):
    to_account = api_manager.user_steps.create_account(create_user_request)
    transfer_request = AccountTransferRequest(fromAccountId=create_deposit_request.id, toAccountId=to_account.id, amount=1000)
    return transfer_request

# Создание юзера с ролью ROLE_CREDIT_SECRET.
@pytest.fixture
def create_credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)
    return user_request

# Создание счёта для юзера с ролью ROLE_CREDIT_SECRET.
@pytest.fixture
def create_credit_account(api_manager, create_credit_user_request):
    return api_manager.user_steps.create_account(create_credit_user_request)

# Запрос на кредит.
@pytest.fixture
def create_credit_request(create_credit_account):
    return AccountCreditRequest(accountId=create_credit_account.id, amount=7500, termMonths=12)

# Запрос на кредит от юзера без нужной роли.
@pytest.fixture
def create_credit_request_wrong_role(create_account):
    return AccountCreditRequest(accountId=create_account.id, amount=12000, termMonths=12)

# Создание кредита — возвращает creditId, amount, balance.
@pytest.fixture
def create_credit_response(api_manager, create_credit_user_request, create_credit_request):
    return api_manager.user_steps.create_credit(create_credit_user_request, create_credit_request)

# Полное погашение кредита.
@pytest.fixture
def create_credit_repay_request(create_credit_account, create_credit_response):
    return AccountCreditRepayRequest(accountId=create_credit_account.id, creditId=create_credit_response.creditId, amount=create_credit_response.amount)