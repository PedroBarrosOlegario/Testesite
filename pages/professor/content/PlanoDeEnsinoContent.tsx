
import React, { useState } from 'react';
import { generateSyllabusWithAI } from '../../../services/geminiService';
import type { PlanoDeEnsino } from '../../../types';
import { SparklesIcon } from '../../../components/icons';

const mockDisciplinas = [
    { id: 1, name: 'Cálculo I', description: 'Introdução ao cálculo diferencial e integral.' },
    { id: 2, name: 'Algoritmos e Estrutura de Dados', description: 'Conceitos fundamentais de algoritmos.' },
];

export default function PlanoDeEnsinoContent() {
    const [selectedDisciplinaId, setSelectedDisciplinaId] = useState<number>(mockDisciplinas[0].id);
    const [plano, setPlano] = useState<Partial<PlanoDeEnsino>>({
        ementa: '', objetivo: '', conteudo: '', referencias: ''
    });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleGenerateWithAI = async () => {
        const disciplina = mockDisciplinas.find(d => d.id === selectedDisciplinaId);
        if (!disciplina) return;
        
        setIsLoading(true);
        setError('');
        try {
            const generatedContent = await generateSyllabusWithAI(disciplina.name, disciplina.description);
            setPlano(generatedContent);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setPlano(prev => ({...prev, [name]: value}));
    }

    return (
        <div className="container mx-auto">
            <div className="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6">
                <div className="flex justify-between items-center mb-6 border-b pb-4 dark:border-gray-700">
                    <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">Plano de Ensino</h2>
                    <button 
                        onClick={handleGenerateWithAI}
                        disabled={isLoading}
                        className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed"
                    >
                        {isLoading ? (
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        ) : (
                           <SparklesIcon className="w-5 h-5 mr-2" />
                        )}
                        {isLoading ? 'Gerando...' : 'Gerar com IA'}
                    </button>
                </div>

                {error && <div className="mb-4 p-4 text-sm text-red-700 bg-red-100 rounded-lg dark:bg-red-200 dark:text-red-800" role="alert">{error}</div>}

                <form className="space-y-6">
                    <div>
                        <label htmlFor="disciplina" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Disciplina</label>
                        <select 
                            id="disciplina" 
                            value={selectedDisciplinaId}
                            onChange={(e) => setSelectedDisciplinaId(Number(e.target.value))}
                            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                        >
                            {mockDisciplinas.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
                        </select>
                    </div>
                    
                    <div>
                        <label htmlFor="ementa" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Ementa</label>
                        <textarea id="ementa" name="ementa" value={plano.ementa} onChange={handleInputChange} rows={4} className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white" placeholder="Descrição resumida do conteúdo da disciplina..."></textarea>
                    </div>
                     <div>
                        <label htmlFor="objetivo" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Objetivo</label>
                        <textarea id="objetivo" name="objetivo" value={plano.objetivo} onChange={handleInputChange} rows={4} className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white" placeholder="Objetivos de aprendizagem para os alunos..."></textarea>
                    </div>
                     <div>
                        <label htmlFor="conteudo" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Conteúdo Programático</label>
                        <textarea id="conteudo" name="conteudo" value={plano.conteudo} onChange={handleInputChange} rows={6} className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white" placeholder="Tópicos e unidades a serem cobertos..."></textarea>
                    </div>
                    <div>
                        <label htmlFor="referencias" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Referências Bibliográficas</label>
                        <textarea id="referencias" name="referencias" value={plano.referencias} onChange={handleInputChange} rows={4} className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white" placeholder="Livros, artigos e outros materiais..."></textarea>
                    </div>

                    <div className="flex justify-end">
                        <button type="submit" className="px-5 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                            Salvar Plano de Ensino
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
