# 1. Core Models (Fundação e Segurança)
from .core.user_model import User
from .core.agente_model import Agente
from .core.unidade_model import Unidade
from .core.usuario_unidade_model import UsuarioUnidade
from .core.orgao_model import Orgao  # <--- NOVO (Criado agora)
from .core.perfil_model import Perfil
from .core.log_auditoria_model import LogAuditoria
from .core.log_documento_model import LogDocumento

# 2. Planejamento Models (Fase Interna / IA)
from .planejamento.modalidade_model import Modalidade
from .planejamento.numero_modalidade_model import NumeroModalidade

from .planejamento.dfd_model import DFD
from .planejamento.item_dfd_model import ItemDFD
from .planejamento.dfd_equipe_model import DFDEquipe
from .planejamento.dfd_dotacao_model import DFDDotacao

from .planejamento.etp_model import ETP
from .planejamento.item_etp_model import ItemETP
from .planejamento.etp_equipe_model import ETPEquipe
from .planejamento.etp_dotacao_model import ETPDotacao

from .planejamento.matriz_risco_model import MatrizRisco
from .planejamento.item_risco_model import ItemRisco
from .planejamento.tr_model import TR

from .planejamento.processo_licitatorio_model import ProcessoLicitatorio
from .planejamento.processo_documento_model import ProcessoDocumento
from .planejamento.template_model import Template

# 3. Gestão Models (Execução e Contratos)
from .gestao.anexo_model import Anexo
from .gestao.tipo_documento_model import TipoDocumento
from .gestao.categoria_model import Categoria
from .gestao.grupo_model import Grupo
from .gestao.subgrupo_model import Subgrupo
from .gestao.catalogo_item_model import CatalogoItem # <--- Importante verificar se o nome da classe é esse mesmo

from .gestao.fornecedor_model import Fornecedor
from .gestao.dotacao_model import Dotacao
from .gestao.local_model import Local

from .gestao.contrato_model import Contrato
from .gestao.instrumento_model import InstrumentoContratual
from .gestao.item_model import ItemContrato

from .gestao.pedido_model import Pedido # Antigo Aocs (Verificar se renomeamos a classe)
from .gestao.itens_aocs_model import ItensAocs
from .gestao.ci_pagamento_model import CiPagamento
from .gestao.aocs_model import Aocs # Mantendo compatibilidade se a classe ainda se chama Aocs