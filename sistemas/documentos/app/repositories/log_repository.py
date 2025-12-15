from sqlalchemy.orm import Session
from app.models.log_model import GenerationLog
import sys

class LogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_log(self, user_id: int, template_id: int, filename: str):
        """
        Registra que um documento foi gerado.
        Não recebe Schema, recebe os dados brutos processados pelo Controller.
        """
        try:
            new_log = GenerationLog(
                user_id=user_id,
                template_id=template_id,
                generated_filename=filename
            )
            self.db.add(new_log)
            self.db.commit()
            self.db.refresh(new_log)
            return new_log
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao criar log: {e}", file=sys.stderr)
            raise e

    def list_by_user(self, user_id: int):
        """Histórico de gerações de um usuário específico."""
        return self.db.query(GenerationLog).filter(GenerationLog.user_id == user_id).all()