import { google } from '@ai-sdk/google';
import { Agent } from '@mastra/core/agent';
import { Memory } from '@mastra/memory';
import { LibSQLStore } from '@mastra/libsql';

export const steamAgent = new Agent({
  name: 'Steam Agent',
  instructions: `
      Sen bir Steam analiz asistanısın. Kullanıcıdan gelen sorularda, gerekirse MCP tool'larını kullanarak veri çekebilirsin.
      Eğer bir Steam istatistiği veya oyun verisi sorulursa, ilgili MCP tool'unu çağır.
      Sonucu kullanıcıya Türkçe ve açıklayıcı şekilde sun.
  `,
  model: google('gemini-1.5-pro-latest'),
  memory: new Memory({
    storage: new LibSQLStore({
      url: 'file:../mastra.db',
    }),
  }),
}); 