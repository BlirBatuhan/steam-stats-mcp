import { detectToolAndParams, runMcpTool } from './utils/mcp-tools';
import { steamAgent } from './agents/steam-agent';

export async function steamHandler(userInput: string) {
  const toolInfo = detectToolAndParams(userInput);
  let mcpResult: any = null;
  let geminiInput = userInput;

  if (toolInfo) {
    mcpResult = await runMcpTool(toolInfo.tool, toolInfo.params);
    geminiInput = `\nKullanıcı sorusu: ${userInput}\nMCP'den gelen veri: ${JSON.stringify(mcpResult)}\nLütfen bu veriyi Türkçe ve açıklayıcı şekilde özetle.`;
  }

  // Gemini ile yanıt üret
  let response;
  if (steamAgent.model && typeof (steamAgent.model as any).invoke === 'function') {
    response = await (steamAgent.model as any).invoke({ messages: [{ role: "user", content: geminiInput }] });
  } else {
    throw new Error('Gemini model fonksiyonu bulunamadı!');
  }
  return response;
} 