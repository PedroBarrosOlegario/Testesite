
import { GoogleGenAI, Type } from "@google/genai";
import type { PlanoDeEnsino } from '../types';

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY as string });

export const generateSyllabusWithAI = async (
  disciplineName: string,
  disciplineDescription: string
): Promise<Partial<PlanoDeEnsino>> => {
  try {
    const prompt = `Gere um plano de ensino para a disciplina "${disciplineName}".
    Descrição da disciplina: "${disciplineDescription}".
    O plano de ensino deve incluir uma ementa, objetivo, conteúdo programático e referências bibliográficas.
    Responda em formato JSON.`;

    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            ementa: { type: Type.STRING },
            objetivo: { type: Type.STRING },
            conteudo: { type: Type.STRING },
            referencias: { type: Type.STRING },
          },
        },
      },
    });

    const jsonText = response.text.trim();
    const generatedContent = JSON.parse(jsonText);

    return generatedContent as Partial<PlanoDeEnsino>;

  } catch (error) {
    console.error("Error generating syllabus with AI:", error);
    throw new Error("Failed to generate syllabus. Please check your API key and try again.");
  }
};
