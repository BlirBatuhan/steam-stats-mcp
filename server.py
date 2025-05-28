from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

mcp = FastMCP("steam-stats-mcp")

STEAM_API_URL = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
STEAM_STORE_API = "https://store.steampowered.com/api/appdetails"
STEAM_USER_API = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
STEAM_USER_STATS_API = "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/"

# Popüler oyunların app_id'leri
POPULAR_GAMES = {
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

async def get_steam_stats(app_id: str) -> Dict[str, Any]:
    """Steam'den oyun istatistiklerini çeker"""
    try:
        response = requests.get(f"{STEAM_API_URL}?appid={app_id}")
        data = response.json()
        
        # Oyun detaylarını al
        store_response = requests.get(f"{STEAM_STORE_API}?appids={app_id}")
        store_data = store_response.json()
        
        game_name = store_data[app_id]["data"]["name"] if store_data[app_id]["success"] else "Bilinmeyen Oyun"
        genres = store_data[app_id]["data"].get("genres", []) if store_data[app_id]["success"] else []
        
        return {
            "game_name": game_name,
            "current_players": data["response"]["player_count"],
            "genres": [genre["description"] for genre in genres],
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
    results = []
    for app_id, game_name in POPULAR_GAMES.items():
        stats = await get_steam_stats(app_id)
        if stats["status"] == "success":
            results.append({
                "game_name": stats["game_name"],
                "current_players": stats["current_players"],
                "genres": stats["genres"]
            })
    
    # Oyuncu sayısına göre sırala
    results.sort(key=lambda x: x["current_players"], reverse=True)
    
    return {
        "status": "success",
        "games": results[:10]  # En çok oynanan 10 oyunu döndür
    }

@mcp.tool()
async def get_game_genres(app_id: str) -> Dict[str, Any]:
    """
    Belirli bir oyunun türlerini döndürür
    """
    try:
        store_response = requests.get(f"{STEAM_STORE_API}?appids={app_id}")
        store_data = store_response.json()
        
        if not store_data[app_id]["success"]:
            return {
                "status": "error",
                "error": "Oyun bulunamadı"
            }
        
        game_name = store_data[app_id]["data"]["name"]
        genres = [genre["description"] for genre in store_data[app_id]["data"].get("genres", [])]
        
        return {
            "status": "success",
            "game_name": game_name,
            "genres": genres
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@mcp.tool()
async def get_popular_genres() -> Dict[str, Any]:
    """
    En popüler oyun türlerini ve oyuncu sayılarını döndürür
    """
    genre_stats = Counter()
    genre_games = Counter()
    
    for app_id in POPULAR_GAMES.keys():
        stats = await get_steam_stats(app_id)
        if stats["status"] == "success":
            for genre in stats["genres"]:
                genre_stats[genre] += stats["current_players"]
                genre_games[genre] += 1
    
    # En popüler türleri bul
    top_genres = []
    for genre, player_count in genre_stats.most_common():
        top_genres.append({
            "genre": genre,
            "total_players": player_count,
            "game_count": genre_games[genre]
        })
    
    return {
        "status": "success",
        "genres": top_genres[:10]  # En popüler 10 türü döndür
    }

@mcp.tool()
async def get_player_stats(steam_id: str) -> Dict[str, Any]:
    """
    Oyuncunun son oynadığı oyunu ve istatistiklerini döndürür
    """
    try:
        # Steam API anahtarını al
        api_key = os.getenv("STEAM_API_KEY", "08C4CB50698FCCE935AC18AFB08EB432")
        if not api_key:
            return {
                "status": "error",
                "error": "Steam API anahtarı bulunamadı"
            }

        # Oyuncu bilgilerini al
        user_response = requests.get(f"{STEAM_USER_API}?key={api_key}&steamids={steam_id}")
        user_data = user_response.json()

        if not user_data["response"]["players"]:
            return {
                "status": "error",
                "error": "Oyuncu bulunamadı"
            }

        player = user_data["response"]["players"][0]
        
        # Son oynanan oyunu al
        last_game = None
        if "gameextrainfo" in player:
            last_game = {
                "name": player["gameextrainfo"],
                "app_id": player.get("gameid", "unknown")
            }

        # Oyuncu istatistiklerini al
        stats = {}
        if last_game and last_game["app_id"] != "unknown":
            stats_response = requests.get(
                f"{STEAM_USER_STATS_API}?appid={last_game['app_id']}&key={api_key}&steamid={steam_id}"
            )
            stats_data = stats_response.json()
            
            if "playerstats" in stats_data and "stats" in stats_data["playerstats"]:
                stats = {
                    stat["name"]: stat["value"]
                    for stat in stats_data["playerstats"]["stats"]
                }

        return {
            "status": "success",
            "player_name": player["personaname"],
            "last_game": last_game,
            "stats": stats,
            "profile_url": player["profileurl"]
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run(transport="stdio")