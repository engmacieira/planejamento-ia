from sqlalchemy.orm import Session
from app.repositories.gestao.contrato_repository import ContratoRepository
# from app.schemas.gestao.contrato_schema import ContratoCreate # TODO: Verify schema
# from app.models.gestao.contrato_model import Contrato

class ContratoService:
    def create_contrato(self, db: Session, contrato_in):
        if contrato_in.data_fim_vigencia and contrato_in.data_inicio_vigencia:
            if contrato_in.data_fim_vigencia < contrato_in.data_inicio_vigencia:
                raise ValueError("A data final de vigência não pode ser anterior à data inicial.")
        
        repo = ContratoRepository(db)
        # Implement logic
        return repo.create(contrato_in)

    def get_contratos_vencendo(self, db: Session, days: int = 30):
        repo = ContratoRepository(db)
        # Placeholder for logic to find contracts expiring in X days
        # This would require a repository method like get_expiring(days)
        return [] 

    def calcular_saldo(self, db: Session, contrato_id: int):
        repo = ContratoRepository(db)
        # Placeholder for calculating balance
        # contrato = repo.get_by_id(contrato_id)
        # ... logic ...
        return 0.0
