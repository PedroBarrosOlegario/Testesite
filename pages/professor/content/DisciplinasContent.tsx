
import React, { useState } from 'react';
import type { Disciplina } from '../../../types';

const mockDisciplinas: Disciplina[] = [
    { id: 1, name: 'Cálculo I', sigla: 'MAT101', descricao: 'Introdução ao cálculo diferencial e integral.', cargaHoraria: 90 },
    { id: 2, name: 'Algoritmos e Estrutura de Dados', sigla: 'CSC101', descricao: 'Conceitos fundamentais de algoritmos.', cargaHoraria: 120 },
    { id: 3, name: 'Física Clássica', sigla: 'FIS101', descricao: 'Leis de Newton e conservação de energia.', cargaHoraria: 90 },
    { id: 4, name: 'Introdução à Filosofia', sigla: 'FIL101', descricao: 'Pensadores clássicos.', cargaHoraria: 60 },
];

export default function DisciplinasContent() {
    const [disciplinas, setDisciplinas] = useState<Disciplina[]>(mockDisciplinas);

    return (
        <div className="container mx-auto">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">Gerenciar Disciplinas</h2>
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Criar Disciplina
                </button>
            </div>

            <div className="bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="min-w-full text-sm text-left text-gray-500 dark:text-gray-400">
                        <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                            <tr>
                                <th scope="col" className="px-6 py-3">Nome</th>
                                <th scope="col" className="px-6 py-3">Sigla</th>
                                <th scope="col" className="px-6 py-3">Carga Horária</th>
                                <th scope="col" className="px-6 py-3">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {disciplinas.map((disciplina) => (
                                <tr key={disciplina.id} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                                    <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                        {disciplina.name}
                                    </th>
                                    <td className="px-6 py-4">{disciplina.sigla}</td>
                                    <td className="px-6 py-4">{disciplina.cargaHoraria}h</td>
                                    <td className="px-6 py-4 flex space-x-2">
                                        <button className="font-medium text-blue-600 dark:text-blue-500 hover:underline">Editar</button>
                                        <button className="font-medium text-red-600 dark:text-red-500 hover:underline">Excluir</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
