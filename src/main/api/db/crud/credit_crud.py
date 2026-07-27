from sqlalchemy.orm import Session

from src.main.api.db.models.credit_table import Credit


class CreditCrudDb:
    @staticmethod
    def get_credit_by_to_account_id(db: Session, id: int) -> Credit | None:
        return db.query(Credit).filter_by(account_id=id).first()