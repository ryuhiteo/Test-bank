from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_to_account_id(db: Session, id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=id).first()
