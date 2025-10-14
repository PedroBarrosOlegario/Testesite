import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import ArtemisLogo from '../../components/ArtemisLogo';
import { HomeIcon, BookOpenIcon, UsersIcon, AcademicCapIcon, ClipboardListIcon, UserCircleIcon, LogoutIcon } from '../../components/icons';
import DashboardContent from './content/DashboardContent';
import DisciplinasContent from './content/DisciplinasContent';
import PlanoDeEnsinoContent from './content/PlanoDeEnsinoContent';
import type { User } from '../../App';

// Placeholder components for other pages
const TurmasContent = () => <div className="text-white">Gerenciamento de Turmas</div>;
const CursosContent = () => <div className="text-white">Gerenciamento de Cursos</div>;
const AlunosContent = () => <div className="text-white">Visualização de Alunos</div>;
const ProfileContent = () => <div className="text-white">Configurações Pessoais</div>;


const navItems = [
    { name: 'Dashboard', path: '/professor', icon: HomeIcon, component: DashboardContent },
    { name: 'Disciplinas', path: '/professor/disciplinas', icon: BookOpenIcon, component: DisciplinasContent },
    { name: 'Turmas', path: '/professor/turmas', icon: UsersIcon, component: TurmasContent },
    { name: 'Cursos', path: '/professor/cursos', icon: AcademicCapIcon, component: CursosContent },
    { name: 'Alunos', path: '/professor/alunos', icon: UsersIcon, component: AlunosContent },
    { name: 'Plano de Ensino', path: '/professor/plano-de-ensino', icon: ClipboardListIcon, component: PlanoDeEnsinoContent },
    { name: 'Meu Perfil', path: '/professor/perfil', icon: UserCircleIcon, component: ProfileContent },
];

const Sidebar: React.FC<{ onLogout: () => void }> = ({ onLogout }) => {
    const location = useLocation();

    return (
        <aside className="w-64 flex-shrink-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
            <div className="h-16 flex items-center justify-center px-4 border-b border-gray-200 dark:border-gray-700">
                <ArtemisLogo />
            </div>
            <nav className="flex-1 px-2 py-4 space-y-1">
                {navItems.map(item => {
                    const isActive = location.pathname === item.path || (item.path === '/professor' && location.pathname.startsWith('/professor/'));
                    return (
                        <Link key={item.name} to={item.path} className={`flex items-center px-4 py-2.5 text-sm font-medium rounded-lg transition-colors duration-200 ${isActive ? 'bg-blue-500 text-white' : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'}`}>
                            <item.icon className="w-5 h-5 mr-3" />
                            {item.name}
                        </Link>
                    );
                })}
            </nav>
            <div className="px-2 py-4 mt-auto">
                 <button onClick={onLogout} className="flex items-center w-full px-4 py-2.5 text-sm font-medium text-gray-600 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                    <LogoutIcon className="w-5 h-5 mr-3" />
                    Sair
                </button>
            </div>
        </aside>
    );
};

const Header: React.FC<{ userName: string }> = ({ userName }) => {
    const location = useLocation();
    const currentNavItem = navItems.find(item => item.path === location.pathname);
    const title = currentNavItem ? currentNavItem.name : 'Dashboard';

    return (
        <header className="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6">
            <h1 className="text-xl font-semibold text-gray-900 dark:text-white">{title}</h1>
            <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600 dark:text-gray-300">Prof. {userName}</span>
                <img className="h-8 w-8 rounded-full object-cover" src="https://picsum.photos/100" alt="User" />
            </div>
        </header>
    );
};


export default function ProfessorDashboard({ user, onLogout }: { user: User; onLogout: () => void }) {
    return (
        <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
            <Sidebar onLogout={onLogout} />
            <div className="flex-1 flex flex-col overflow-hidden">
                <Header userName={user.name} />
                <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 dark:bg-gray-900 p-6">
                    <Routes>
                        <Route path="/" element={<DashboardContent />} />
                        <Route path="/disciplinas" element={<DisciplinasContent />} />
                        <Route path="/turmas" element={<TurmasContent />} />
                        <Route path="/cursos" element={<CursosContent />} />
                        <Route path="/alunos" element={<AlunosContent />} />
                        <Route path="/plano-de-ensino" element={<PlanoDeEnsinoContent />} />
                        <Route path="/perfil" element={<ProfileContent />} />
                    </Routes>
                </main>
            </div>
        </div>
    );
}