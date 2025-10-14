import React, { useState } from 'react';
import type { User } from '../App';
import ArtemisLogo from '../components/ArtemisLogo';
import { ArrowLeftIcon, UserCircleIcon, AcademicCapIcon } from '../components/icons';

type View = 'initial' | 'login-aluno' | 'register-aluno' | 'login-professor' | 'register-professor';

interface LandingPageProps {
  onLogin: (user: User) => void;
}

const AuthForm: React.FC<{ isRegister?: boolean, role: 'Aluno' | 'Professor', onBack: () => void, onAuth: (name?: string) => void }> = ({ isRegister, role, onBack, onAuth }) => {
    const [name, setName] = useState('');
    
    return (
        <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700 animate-fade-in">
            <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
                <button onClick={onBack} className="flex items-center text-sm font-medium text-blue-600 hover:underline dark:text-blue-500 mb-4">
                    <ArrowLeftIcon className="w-4 h-4 mr-2"/>
                    Voltar
                </button>
                <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                    {isRegister ? 'Criar conta de' : 'Entrar como'} {role}
                </h1>
                <form className="space-y-4 md:space-y-6" action="#" onSubmit={(e) => { e.preventDefault(); onAuth(isRegister ? name : undefined); }}>
                    {isRegister && (
                        <div>
                            <label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Nome Completo</label>
                            <input type="text" name="name" id="name" value={name} onChange={(e) => setName(e.target.value)} className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white" placeholder="Seu Nome" required />
                        </div>
                    )}
                    <div>
                        <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Email ou Matrícula</label>
                        <input type="email" name="email" id="email" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white" placeholder="nome@email.com" required />
                    </div>
                    <div>
                        <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Senha</label>
                        <input type="password" name="password" id="password" placeholder="••••••••" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white" required />
                    </div>
                    {isRegister && (
                         <div>
                            <label htmlFor="confirm-password" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Confirmar Senha</label>
                            <input type="password" name="confirm-password" id="confirm-password" placeholder="••••••••" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white" required />
                        </div>
                    )}
                    <button type="submit" className="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">{isRegister ? 'Cadastrar' : 'Entrar'}</button>
                </form>
            </div>
        </div>
    );
};

const RoleSelector: React.FC<{ setView: (view: View) => void }> = ({ setView }) => (
    <div className="w-full max-w-4xl bg-white rounded-lg shadow-xl dark:bg-gray-800 dark:border-gray-700 p-8 md:p-12 animate-fade-in">
        <div className="text-center mb-10">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Bem-vindo ao Artemis</h1>
            <p className="text-gray-500 dark:text-gray-400">Selecione seu perfil para continuar</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Aluno Card */}
            <div className="flex flex-col items-center p-6 border border-gray-200 dark:border-gray-700 rounded-lg text-center">
                <div className="bg-blue-100 dark:bg-blue-900 p-4 rounded-full mb-4">
                    <UserCircleIcon className="w-10 h-10 text-blue-600 dark:text-blue-400" />
                </div>
                <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-2">Sou Aluno</h2>
                <p className="text-gray-500 dark:text-gray-400 mb-6">Acesse suas notas, disciplinas e materiais de aula.</p>
                <div className="flex flex-col sm:flex-row gap-4 w-full">
                    <button onClick={() => setView('login-aluno')} className="flex-1 text-white bg-blue-600 hover:bg-blue-700 font-medium rounded-lg text-sm px-5 py-2.5">Entrar</button>
                    <button onClick={() => setView('register-aluno')} className="flex-1 text-blue-700 dark:text-blue-400 bg-blue-100 dark:bg-gray-700 hover:bg-blue-200 dark:hover:bg-gray-600 font-medium rounded-lg text-sm px-5 py-2.5">Cadastrar</button>
                </div>
            </div>
            {/* Professor Card */}
            <div className="flex flex-col items-center p-6 border border-gray-200 dark:border-gray-700 rounded-lg text-center">
                <div className="bg-indigo-100 dark:bg-indigo-900 p-4 rounded-full mb-4">
                     <AcademicCapIcon className="w-10 h-10 text-indigo-600 dark:text-indigo-400" />
                </div>
                <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-2">Sou Professor</h2>
                <p className="text-gray-500 dark:text-gray-400 mb-6">Gerencie suas turmas, planos de ensino e alunos.</p>
                <div className="flex flex-col sm:flex-row gap-4 w-full">
                    <button onClick={() => setView('login-professor')} className="flex-1 text-white bg-indigo-600 hover:bg-indigo-700 font-medium rounded-lg text-sm px-5 py-2.5">Entrar</button>
                    <button onClick={() => setView('register-professor')} className="flex-1 text-indigo-700 dark:text-indigo-400 bg-indigo-100 dark:bg-gray-700 hover:bg-indigo-200 dark:hover:bg-gray-600 font-medium rounded-lg text-sm px-5 py-2.5">Cadastrar</button>
                </div>
            </div>
        </div>
    </div>
);

export default function LandingPage({ onLogin }: LandingPageProps) {
  const [view, setView] = useState<View>('initial');

  const handleAuth = (role: 'aluno' | 'professor', isRegister: boolean, name?: string) => {
    if (isRegister) {
      onLogin({ role, name: name || (role === 'aluno' ? 'Novo Aluno' : 'Novo Professor') });
    } else {
      // In a real app, we'd fetch the user's name after login.
      // For this demo, we'll use a generic name.
      onLogin({ role, name: role === 'aluno' ? 'Aluno(a)' : 'Professor(a)' });
    }
  };


  const renderContent = () => {
    switch (view) {
      case 'login-aluno':
        return <AuthForm role="Aluno" onBack={() => setView('initial')} onAuth={() => handleAuth('aluno', false)} />;
      case 'register-aluno':
        return <AuthForm isRegister role="Aluno" onBack={() => setView('initial')} onAuth={(name) => handleAuth('aluno', true, name)} />;
      case 'login-professor':
        return <AuthForm role="Professor" onBack={() => setView('initial')} onAuth={() => handleAuth('professor', false)} />;
      case 'register-professor':
        return <AuthForm isRegister role="Professor" onBack={() => setView('initial')} onAuth={(name) => handleAuth('professor', true, name)} />;
      case 'initial':
      default:
        return <RoleSelector setView={setView} />;
    }
  };

  return (
    <section className="bg-gray-50 dark:bg-gray-900">
      <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
        <div className="mb-6 md:mb-8">
            <ArtemisLogo className="w-auto h-12" />
        </div>
        {renderContent()}
      </div>
    </section>
  );
}