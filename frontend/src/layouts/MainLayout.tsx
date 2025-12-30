
import { Outlet, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, FileText, Briefcase, Gavel, LogOut } from 'lucide-react';
import clsx from 'clsx';

const SidebarItem = ({ to, icon: Icon, label }: { to: string, icon: any, label: string }) => {
  const location = useLocation();
  const isActive = location.pathname.startsWith(to);

  return (
    <Link
      to={to}
      className={clsx(
        "flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg transition-colors",
        isActive
          ? "bg-blue-50 text-blue-700"
          : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
      )}
    >
      <Icon size={20} />
      {label}
    </Link>
  );
};

export const MainLayout = () => {
  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
        <div className="p-6 border-b border-slate-100">
          <h1 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            Planejamento IA
          </h1>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          <SidebarItem to="/dashboard" icon={LayoutDashboard} label="Dashboard" />
          <SidebarItem to="/licitacao" icon={Gavel} label="Licitação" />
          <SidebarItem to="/gestao" icon={Briefcase} label="Gestão Contratos" />
          <SidebarItem to="/documentos" icon={FileText} label="Documentos" />
        </nav>

        <div className="p-4 border-t border-slate-100">
          <button className="flex items-center gap-3 px-4 py-3 text-sm font-medium text-red-600 rounded-lg hover:bg-red-50 w-full transition-colors">
            <LogOut size={20} />
            Sair
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <header className="bg-white border-b border-slate-200 px-8 py-4 sticky top-0 z-10">
          <h2 className="text-lg font-semibold text-slate-800">Bem-vindo</h2>
        </header>
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
