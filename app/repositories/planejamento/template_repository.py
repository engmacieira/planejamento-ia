from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging
import sys

from app.models.planejamento.template_model import Template
from app.schemas.planejamento.template_schema import TemplateCreate
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class TemplateRepository(BaseRepository[Template, TemplateCreate, TemplateCreate]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Template, db_session)

    async def create_template(self, schema: TemplateCreate, saved_path: str, owner_id: int):
        try:
            db_template = Template(
                filename=schema.filename,
                description=schema.description,
                path=saved_path, # Caminho gerado pelo backend
                owner_id=owner_id
            )
            self.db_session.add(db_template)
            await self.db_session.commit()
            await self.db_session.refresh(db_template)
            return db_template
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro ao criar template: {e}")
            raise e

    async def list_by_user(self, owner_id: int):
        """Lista apenas templates ativos (não deletados) de um usuário."""
        result = await self.db_session.execute(
            select(Template).where(
                Template.owner_id == owner_id,
                Template.is_deleted == False
            )
        )
        return result.scalars().all()

    async def get_by_id(self, template_id: int):
        # Override to ensure we can get by ID using generic BaseRepo if needed, or keeping custom.
        # But BaseRepo 'get' works. Existing code had get_by_id.
        return await self.get(template_id)

    async def delete(self, id: int):
        """Soft Delete: Marca como deletado."""
        try:
            template = await self.get(id)
            if template:
                template.is_deleted = True
                await self.db_session.commit()
                await self.db_session.refresh(template)
                return template
            return None
        except Exception as e:
            await self.db_session.rollback()
            raise e
