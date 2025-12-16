"""ajustes_models

Revision ID: cb869fa5ee74
Revises: ffca60680fa2
Create Date: 2025-12-16 10:27:13.163615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cb869fa5ee74'
down_revision: Union[str, Sequence[str], None] = 'ffca60680fa2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Remover constraints antigas (Manualmente adicionado para corrigir o erro de dependência)
    op.drop_constraint('numeros_modalidade_id_modalidade_fkey', 'numeros_modalidade', type_='foreignkey')
    op.drop_constraint('processos_licitatorios_id_modalidade_fkey', 'processos_licitatorios', type_='foreignkey')

    # 2. Criar a nova tabela 'modalidades'
    op.create_table('modalidades',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('sigla', sa.String(length=10), nullable=True),
        sa.Column('fundamentacao_legal', sa.String(length=255), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=False),
        sa.Column('data_criacao', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome')
    )

    # 3. Remover a tabela antiga 'modalidade' (Agora seguro, pois removemos as constraints no passo 1)
    op.drop_table('modalidade')

    # 4. Adicionar colunas novas em 'contratos' (gerado pelo Alembic)
    op.add_column('contratos', sa.Column('id_categoria', sa.Integer(), nullable=True))
    op.add_column('contratos', sa.Column('id_modalidade', sa.Integer(), nullable=True))
    
    # 5. Criar as novas Foreign Keys
    # FKs de Contratos
    op.create_foreign_key(None, 'contratos', 'categorias', ['id_categoria'], ['id'])
    op.create_foreign_key(None, 'contratos', 'modalidades', ['id_modalidade'], ['id'])
    
    # FKs recriadas para Numeros e Processos (apontando agora para a nova tabela 'modalidades')
    # Nota: Removemos os comandos 'drop_constraint' duplicados daqui, pois já fizemos no passo 1.
    op.create_foreign_key(None, 'numeros_modalidade', 'modalidades', ['id_modalidade'], ['id'])
    op.create_foreign_key(None, 'processos_licitatorios', 'modalidades', ['id_modalidade'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Desfazer as FKs novas
    op.drop_constraint(None, 'processos_licitatorios', type_='foreignkey')
    op.drop_constraint(None, 'numeros_modalidade', type_='foreignkey')
    op.drop_constraint(None, 'contratos', type_='foreignkey')
    op.drop_constraint(None, 'contratos', type_='foreignkey')
    
    # Remover colunas novas
    op.drop_column('contratos', 'id_modalidade')
    op.drop_column('contratos', 'id_categoria')
    
    # Recriar a tabela antiga 'modalidade'
    op.create_table('modalidade',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column('sigla', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
        sa.Column('fundamentacao_legal', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column('ativo', sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column('data_criacao', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('id', name='modalidade_pkey'),
        sa.UniqueConstraint('nome', name='modalidade_nome_key')
    )
    
    # Remover a tabela nova 'modalidades'
    op.drop_table('modalidades')
    
    # Recriar as constraints antigas
    op.create_foreign_key('processos_licitatorios_id_modalidade_fkey', 'processos_licitatorios', 'modalidade', ['id_modalidade'], ['id'])
    op.create_foreign_key('numeros_modalidade_id_modalidade_fkey', 'numeros_modalidade', 'modalidade', ['id_modalidade'], ['id'])