
import React from 'react';
import { UsersIcon, BookOpenIcon, ClipboardListIcon } from '../../../components/icons';

const StatCard: React.FC<{ title: string; value: string | number; icon: React.ElementType }> = ({ title, value, icon: Icon }) => (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md flex items-center space-x-4">
        <div className="bg-blue-100 dark:bg-blue-900 p-3 rounded-full">
            <Icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
        </div>
        <div>
            <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
            <p className="text-2xl font-semibold text-gray-900 dark:text-white">{value}</p>
        </div>
    </div>
);

export default function DashboardContent() {
    return (
        <div className="container mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <StatCard title="Total de Turmas" value={8} icon={UsersIcon} />
                <StatCard title="Total de Alunos" value={124} icon={UsersIcon} />
                <StatCard title="Disciplinas Ativas" value={5} icon={BookOpenIcon} />
                <StatCard title="Planos de Ensino Criados" value={5} icon={ClipboardListIcon} />
            </div>
            {/* Additional dashboard components can be added here */}
        </div>
    );
}
