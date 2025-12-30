from sqlalchemy.orm import Session
from app.models.template_model import Template
from app.schemas.template_schema import TemplateCreate
import sys

class TemplateRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, schema: TemplateCreate, saved_path: str, owner_id: int):
        try:
            db_template = Template(
                filename=schema.filename,
                description=schema.description,
                path=saved_path, # Caminho gerado pelo backend
                owner_id=owner_id
            )
            self.db.add(db_template)
            self.db.commit()
            self.db.refresh(db_template)
            return db_template
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao criar template: {e}", file=sys.stderr)
            raise e

    def list_by_user(self, owner_id: int):
        """Lista apenas templates ativos (não deletados) de um usuário."""
        return self.db.query(Template).filter(
            Template.owner_id == owner_id,
            Template.is_deleted == False  # Regra de Soft Delete na leitura
        ).all()

    def get_by_id(self, template_id: int):
        """Busca um template específico (mesmo que deletado, para histórico)."""
        return self.db.query(Template).filter(Template.id == template_id).first()

    def delete(self, template_id: int):
        """Soft Delete: Marca como deletado e atualiza a data."""
        try:
            template = self.get_by_id(template_id)
            if template:
                template.is_deleted = True
                # O updated_at atualiza sozinho graças ao DefaultModel
                self.db.commit()
                self.db.refresh(template)
            return template
        except Exception as e:
            self.db.rollback()
            raise e