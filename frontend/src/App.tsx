
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainLayout } from './layouts/MainLayout';

// Placeholder pages
const Dashboard = () => <div>Dashboard Content</div>;
const Licitacao = () => <div>Licitação Content</div>;
const Gestao = () => <div>Gestão Content</div>;
const Documentos = () => <div>Documentos Content</div>;
const Login = () => <div>Login Page</div>;

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route path="/" element={<MainLayout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="licitacao/*" element={<Licitacao />} />
            <Route path="gestao/*" element={<Gestao />} />
            <Route path="documentos/*" element={<Documentos />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
