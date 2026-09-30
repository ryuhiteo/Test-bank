from src.main.UI.pages.catalog_page import CatalogPage
from src.main.UI.steps.login_steps import LoginSteps
from src.main.UI.steps.catalog_steps import CatalogSteps

def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0, "Ожидание товаров на странице каталога"

def test_auth_negative(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("locked_out_user", "secret_sauce")

    error_text = steps.login_page.get_error_text()
    assert "locked out" in error_text, "Ожидание сообщения о заблокированном пользователе"

def test_logout(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    catalog.logout()
    assert page.url == "https://www.saucedemo.com/", "Ожидаем возврат на страницу логина"


def test_logout_visual_user(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("visual_user", "secret_sauce")
    assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    catalog.logout()
    assert page.url == login.LOGIN_URL, "Ожидаем возврат на страницу логина"







