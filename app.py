from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn
from server import get_top_games

app = FastAPI(title="Steam İstatistikleri")

class GameStats(BaseModel):
    game_name: str
    current_players: int

class TopGamesResponse(BaseModel):
    status: str
    games: List[GameStats]

@app.get("/top-games", response_model=TopGamesResponse)
async def get_steam_top_games() -> Dict[str, Any]:
    """En çok oynanan Steam oyunlarını döndürür"""
    try:
        result = await get_top_games()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
