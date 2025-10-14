import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import ArtemisLogo from '../../components/ArtemisLogo';
import { HomeIcon, BookOpenIcon, UsersIcon, AcademicCapIcon, UserCircleIcon, LogoutIcon } from '../../components/icons';
import type { User } from '../../App';

// Placeholder components for student pages
const AlunoDashboardContent = () => <div className="text-white">Resumo do Aluno</div>;
const MeusCursosContent = () => <div className="text-white">Meus Cursos</div>;
const MinhasDisciplinasContent = () => <div className="text-white">Minhas Disciplinas</div>;
const MinhasTurmasContent = () => <div className="text-white">Minhas Turmas</div>;
const MeuPerfilContent = () => <div className="text-white">Meu Perfil</div>;

const navItems = [
    { name: 'Dashboard', path: '/aluno', icon: HomeIcon },
    { name: 'Meus Cursos', path: '/aluno/cursos', icon: AcademicCapIcon },
    { name: 'Minhas Disciplinas', path: '/aluno/disciplinas', icon: BookOpenIcon },
    { name: 'Minhas Turmas', path: '/aluno/turmas', icon: UsersIcon },
    { name: 'Meu Perfil', path: '/aluno/perfil', icon: UserCircleIcon },
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
                    const isActive = location.pathname === item.path || (item.path === '/aluno' && location.pathname.startsWith('/aluno/'));
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
                <span className="text-sm text-gray-600 dark:text-gray-300">{userName}</span>
                 <img className="h-8 w-8 rounded-full object-cover" src="https://picsum.photos/101" alt="User" />
            </div>
        </header>
    );
};

export default function AlunoDashboard({ user, onLogout }: { user: User; onLogout: () => void }) {
    return (
        <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
            <Sidebar onLogout={onLogout} />
            <div className="flex-1 flex flex-col overflow-hidden">
                <Header userName={user.name} />
                <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 dark:bg-gray-900 p-6">
                     <Routes>
                        <Route path="/" element={<AlunoDashboardContent />} />
                        <Route path="/cursos" element={<MeusCursosContent />} />
                        <Route path="/disciplinas" element={<MinhasDisciplinasContent />} />
                        <Route path="/turmas" element={<MinhasTurmasContent />} />
                        <Route path="/perfil" element={<MeuPerfilContent />} />
                    </Routes>
                </main>
            </div>
        </div>
    );
}