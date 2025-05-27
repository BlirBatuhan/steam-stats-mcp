from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
import re

mcp = FastMCP("agent-router-mcp")

# Ajan tanımlamaları
FOOD_AGENT = "food-agent"
COACHING_AGENT = "coaching-agent"

def analyze_intent(message: str) -> str:
    """
    Kullanıcı mesajını analiz eder ve uygun ajanı seçer
    """
    # Yemek ile ilgili anahtar kelimeler
    food_keywords = ["yemek", "ne yesem", "akşam", "yemek öner", "tarif"]
    
    # Motivasyon ile ilgili anahtar kelimeler
    coaching_keywords = ["moralsiz", "motivasyon", "koç", "yardım", "destek"]
    
    message = message.lower()
    
    # Yemek ajanı kontrolü
    if any(keyword in message for keyword in food_keywords):
        return FOOD_AGENT
    
    # Koçluk ajanı kontrolü
    if any(keyword in message for keyword in coaching_keywords):
        return COACHING_AGENT
    
    # Varsayılan olarak koçluk ajanına yönlendir
    return COACHING_AGENT

@mcp.tool()
async def route_to_agent(message: str) -> Dict[str, Any]:
    """
    Kullanıcı mesajını analiz eder ve uygun ajanı seçer
    """
    selected_agent = analyze_intent(message)
    
    return {
        "agent": selected_agent,
        "message": message,
        "status": "success"
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")