from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("steam-stats-mcp")

STEAM_API_URL = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
STEAM_STORE_API = "https://store.steampowered.com/api/appdetails"

async def get_steam_stats(app_id: str) -> Dict[str, Any]:
    """Steam'den oyun istatistiklerini çeker"""
    try:
        response = requests.get(f"{STEAM_API_URL}?appid={app_id}")
        data = response.json()
        
        # Oyun detaylarını al
        store_response = requests.get(f"{STEAM_STORE_API}?appids={app_id}")
        store_data = store_response.json()
        
        game_name = store_data[app_id]["data"]["name"] if store_data[app_id]["success"] else "Bilinmeyen Oyun"
        
        return {
            "game_name": game_name,
            "current_players": data["response"]["player_count"],
            "status": "success"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@mcp.tool()
async def get_top_games() -> Dict[str, Any]:
    """
    Steam'in en çok oynanan oyunlarını ve oyuncu sayılarını döndürür
    """
    # En popüler Steam oyunlarının app_id'leri
    popular_games = {
        "730": "CS2",
        "570": "Dota 2",
        "1172470": "Apex Legends",
        "578080": "PUBG: BATTLEGROUNDS",
        "252490": "Rust",
        "1085660": "Destiny 2",
        "1091500": "Cyberpunk 2077",
        "1174180": "Red Dead Redemption 2",
        "1172470": "Apex Legends",
        "1174180": "Red Dead Redemption 2"
    }
    
    results = []
    for app_id, game_name in popular_games.items():
        stats = await get_steam_stats(app_id)
        if stats["status"] == "success":
            results.append({
                "game_name": stats["game_name"],
                "current_players": stats["current_players"]
            })
    
    # Oyuncu sayısına göre sırala
    results.sort(key=lambda x: x["current_players"], reverse=True)
    
    return {
        "status": "success",
        "games": results[:10]  # En çok oynanan 10 oyunu döndür
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")