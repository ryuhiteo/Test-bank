from http import HTTPStatus

from requests import Response


class ResponseSpecs:
    # STATUS = 200
    @staticmethod
    def request_ok():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    #STATUS = 201
    @staticmethod
    def request_created():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    #STATUS = 400
    @staticmethod
    def request_bad():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    # STATUS = 401
    @staticmethod
    def request_unauthorized():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text
        return confirm

    # STATUS = 409
    @staticmethod
    def max_accounts_reached():
        def confirm(response: Response):
                assert response.status_code == HTTPStatus.CONFLICT, response.text
        return confirm

    # STATUS = 403
    @staticmethod
    def request_forbidden():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text
        return confirm

    # STATUS = 422
    @staticmethod
    def unprocessable_repayment():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text
        return confirm

