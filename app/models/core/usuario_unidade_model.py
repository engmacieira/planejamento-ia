from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class UsuarioUnidade(Base):
    """
    Tabela Associativa que vincula Usuários a Unidades (N:N).
    Permite que um servidor tenha acesso a múltiplas secretarias.
    """
    __tablename__ = "usuarios_unidades"

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), primary_key=True)
    unidade_id: Mapped[int] = mapped_column(ForeignKey("unidades.id"), primary_key=True)

    def __repr__(self):
        return f"<Link User {self.usuario_id} - Unidade {self.unidade_id}>"