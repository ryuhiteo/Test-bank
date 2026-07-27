import pytest
from sqlalchemy.orm.session import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateUser:
    # Тест на создание юзера.
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
    )
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        # Запрос на создание юзера.
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, 'Ошибка: созданный пользователь не найден.'


    # Негативный тест на создание юзера.
    @pytest.mark.parametrize(
        "username, password",
        [
            # Негативная проверка по логину.
            ("Борис", "Pas!sw0rd"), # Только латиница
            ("Vi", "Pas!sw0rd"), # Минимум 3 символа
            ("BorkusBorkusBorkus", "Pas!sw0rd"), # Максимум 15 символов
            ("Larison!", "Pas!sw0rd"), # Запрещены спец.символы

            # Негативная проверка по паролю
            ("Viper", "Pas!sw0rdЫ"), # Только латиница
            ("Johny", "Pas!sw0"), # От 8-ми символов
            ("Lepesh", "pas!sw0r"), # Минимум 1 заглавная буква
            ("Sasko", "PAS!SW0R"), # Минимум 1 маленькая буква
            ("Fresco", "Passw0rdd"),  # Минимум 1 спец. символ
            ("Gordon", "Passwordd"), # Минимум 1 цифра
        ]
    )
    def test_create_user_invalid(self, db_session: Session, username: str, password: str, api_manager: ApiManager):
        # Запрос на создание пользователя.
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid(create_user_request) # Ловим ошибки.

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is None, 'Ошибка: пользователь создан.'
