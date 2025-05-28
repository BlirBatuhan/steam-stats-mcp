import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
// Eğer @smithery/sdk bulunamazsa, doğrudan URL stringi ile de kullanılabilir.
// import { createSmitheryUrl } from '@smithery/sdk';

const config = {};
const serverUrl =
  "https://server.smithery.ai/@BlirBatuhan/steam-stats-mcp?apiKey=fbc71d09-60a7-429c-92e9-3447ae5a18a3";

const transport = new StreamableHTTPClientTransport(new URL(serverUrl));

const mcpClient = new Client({
  name: "Steam MCP Agent",
  version: "1.0.0"
});

export async function listMcpTools() {
  await mcpClient.connect(transport);
  const tools = await mcpClient.listTools();
  // tools tipi bilinmiyorsa, güvenli şekilde isimlerini döndür
  if (Array.isArray(tools)) {
    return tools.map((t: any) => t.name);
  }
  return [];
}

export async function runMcpTool(toolName: string, params: any) {
  await mcpClient.connect(transport);
  // Doğru parametre yapısı: { name, arguments }
  const result = await mcpClient.callTool({
    name: toolName,
    arguments: params
  });
  return result;
}

export function detectToolAndParams(userInput: string) {
  if (userInput.includes("en çok oynanan oyunlar")) {
    return { tool: "get_top_games", params: {} };
  }
  if (userInput.includes("oyun türleri")) {
    const match = userInput.match(/['"](.+)['"]/) || [];
    const gameName = match[1];
    if (gameName) {
      return { tool: "get_game_genres", params: { game_name: gameName } };
    }
  }
  if (userInput.includes("popüler türler")) {
    return { tool: "get_popular_genres", params: {} };
  }
  if (userInput.includes("oyuncu istatistikleri")) {
    const match = userInput.match(/['"](.+)['"]/) || [];
    const playerName = match[1];
    if (playerName) {
      return { tool: "get_player_stats", params: { player_name: playerName } };
    }
  }
  return null;
} 