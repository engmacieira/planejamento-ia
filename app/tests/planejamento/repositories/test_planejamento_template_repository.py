import pytest
from app.repositories.planejamento.template_repository import TemplateRepository
from app.schemas.planejamento.template_schema import TemplateCreate

@pytest.mark.asyncio
async def test_template_flow(db_session, sample_user):
    repo = TemplateRepository(db_session)
    
    t_in = TemplateCreate(filename="t.docx", description="Desc")
    
    # Create
    tmpl = await repo.create_template(t_in, saved_path="/tmp/t.docx", owner_id=sample_user.id)
    assert tmpl.id is not None
    
    # List
    lst = await repo.list_by_user(sample_user.id)
    assert len(lst) >= 1
    
    # Soft Delete
    deleted = await repo.delete(tmpl.id)
    assert deleted.is_deleted is True
    
    # List again (should be empty if only one existed)
    lst_after = await repo.list_by_user(sample_user.id)
    assert len(lst_after) == 0 # Provided we started fresh or filter works
