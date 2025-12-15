import { useNavigate } from 'react-router-dom';
import { FileText, Calendar, Building2, ArrowRight, Edit } from 'lucide-react'; // Adicionei 'Edit'

// Atualizamos a interface para refletir a realidade do Backend
export interface ProcessoCardProps {
  data: {
    id: number;
    numero?: string;
    ano?: number;
    objeto: string;
    // Agora aceita string (legado) ou objeto (novo backend)
    unidade_requisitante?: string | { nome: string }; 
    status?: string;
    created_at?: string;
  };
}

export function ProcessoCard({ data }: ProcessoCardProps) {
  const navigate = useNavigate();

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Data n/d';
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getStatusColor = (status?: string) => {
    const s = (status || 'Rascunho').toLowerCase();
    if (s === 'concluído') return 'bg-green-100 text-green-700 border-green-200';
    if (s === 'em andamento') return 'bg-blue-100 text-blue-700 border-blue-200';
    return 'bg-gray-100 text-gray-700 border-gray-200';
  };

  // Helper para pegar o nome da unidade com segurança
  const getUnidadeNome = () => {
    if (!data.unidade_requisitante) return 'Unidade não definida';
    if (typeof data.unidade_requisitante === 'string') return data.unidade_requisitante;
    return data.unidade_requisitante.nome;
  };

  return (
    <div className="group bg-white rounded-2xl p-6 border border-gray-200 hover:border-blue-300 hover:shadow-xl transition-all duration-300 flex flex-col justify-between h-full">
      
      {/* --- Topo: Status e Data --- */}
      <div>
        <div className="flex justify-between items-start mb-4">
          <div className={`text-xs font-bold px-3 py-1 rounded-full border ${getStatusColor(data.status)}`}>
            {data.status || 'Rascunho'}
          </div>
          <span className="text-gray-400 text-xs flex items-center gap-1">
            <Calendar size={12} />
            {formatDate(data.created_at)}
          </span>
        </div>

        {/* Título (Objeto) */}
        <h3 className="text-lg font-bold text-gray-800 mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors" title={data.objeto}>
          {data.objeto || 'Objeto não informado'}
        </h3>

        {/* Informações Secundárias */}
        <div className="space-y-2 text-sm text-gray-500 mb-6">
          <div className="flex items-center gap-2">
            <Building2 size={16} className="text-gray-400" />
            <span className="truncate" title={getUnidadeNome()}>
                {getUnidadeNome()}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <FileText size={16} className="text-gray-400" />
            <span>Processo Nº {data.numero || 'S/N'}/{data.ano || 2024}</span>
          </div>
        </div>
      </div>

      {/* --- Rodapé: Ações (Aqui está o que faltava!) --- */}
      <div className="pt-4 border-t border-gray-100 flex justify-between items-center">
        
        {/* Botão EDITAR (Novo) */}
        <button 
          onClick={() => navigate(`/dfd/${data.id}`)}
          className="text-gray-500 hover:text-blue-600 hover:bg-blue-50 p-2 rounded-lg transition-colors flex items-center gap-2 text-sm font-medium"
        >
          <Edit size={16} /> Editar
        </button>

        {/* Botão PLANEJAMENTO */}
        <button 
          onClick={() => navigate(`/planejamento?dfd_id=${data.id}`)}
          className="text-sm font-semibold text-blue-600 flex items-center gap-1 hover:gap-2 transition-all"
        >
          Planejamento <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}