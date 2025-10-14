
export interface Aluno {
  id: number;
  nome: string;
  cpf: string;
  dataNascimento: string;
  email: string;
  matricula: number;
  genero: string;
  curso: string;
}

export interface Professor {
  id: number;
  nome: string;
  cpf: string;
  dataNascimento: string;
  email: string;
  matricula: string;
  genero: string;
}

export interface Curso {
  id: number;
  nome: string;
  sigla: string;
  descricao: string;
  coordenador: string;
}

export interface Disciplina {
  id: number;
  name: string;
  sigla: string;
  descricao: string;
  cargaHoraria: number;
  planoDeEnsino?: string;
}

export interface Turma {
  id: number;
  nome: string;
  codigo: string;
  turno: string;
  curso: string;
  disciplina: string;
  professor: string;
  alunos: number;
}

export interface PlanoDeEnsino {
  id: number;
  disciplinaId: number;
  ementa: string;
  objetivo: string;
  conteudo: string;
  referencias: string;
}
