import pytest
from sqlalchemy.sql import text

@pytest.mark.asyncio
async def test_database_connection(db_session):
    # Try to execute a simple query
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1
