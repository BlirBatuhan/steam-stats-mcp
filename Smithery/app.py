from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn
from server import get_top_games, get_game_genres, get_popular_genres, get_player_stats

app = FastAPI(title="Steam İstatistikleri")

class GameStats(BaseModel):
    game_name: str
    current_players: int
    genres: List[str]

class TopGamesResponse(BaseModel):
    status: str
    games: List[GameStats]

class GameGenresResponse(BaseModel):
    status: str
    game_name: str
    genres: List[str]

class GenreStats(BaseModel):
    genre: str
    total_players: int
    game_count: int

class PopularGenresResponse(BaseModel):
    status: str
    genres: List[GenreStats]

class LastGame(BaseModel):
    name: str
    app_id: str

class PlayerStatsResponse(BaseModel):
    status: str
    player_name: str
    last_game: Optional[LastGame]
    stats: Dict[str, Any]
    profile_url: str

@app.get("/top-games", response_model=TopGamesResponse)
async def get_steam_top_games() -> Dict[str, Any]:
    """En çok oynanan Steam oyunlarını döndürür"""
    try:
        result = await get_top_games()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/game-genres/{app_id}", response_model=GameGenresResponse)
async def get_steam_game_genres(app_id: str) -> Dict[str, Any]:
    """Belirli bir oyunun türlerini döndürür"""
    try:
        result = await get_game_genres(app_id)
        if result["status"] == "error":
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/popular-genres", response_model=PopularGenresResponse)
async def get_steam_popular_genres() -> Dict[str, Any]:
    """En popüler oyun türlerini döndürür"""
    try:
        result = await get_popular_genres()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/{steam_id}", response_model=PlayerStatsResponse)
async def get_steam_player_stats(steam_id: str) -> Dict[str, Any]:
    """Oyuncunun son oynadığı oyunu ve istatistiklerini döndürür"""
    try:
        result = await get_player_stats(steam_id)
        if result["status"] == "error":
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
