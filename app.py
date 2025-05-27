from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from server import route_to_agent, FOOD_AGENT, COACHING_AGENT

app = FastAPI(title="Akıllı Ajan Router")

class Message(BaseModel):
    text: str

# Yemek önerileri için örnek veritabanı
FOOD_DATABASE = {
    "akşam": ["Mercimek Çorbası", "Izgara Köfte", "Pide", "Lahmacun"],
    "öğle": ["Köfte Ekmek", "Döner", "Pizza", "Burger"],
    "kahvaltı": ["Menemen", "Omlet", "Simit", "Börek"]
}

# Motivasyon mesajları için örnek veritabanı
COACHING_DATABASE = {
    "moralsiz": [
        "Her gün yeni bir başlangıçtır. Kendine inan!",
        "Zorluklar seni güçlendirir. Devam et!",
        "Bugün zor bir gün olabilir, ama yarın daha iyi olacak."
    ],
    "motivasyon": [
        "Hedeflerine ulaşmak için her gün bir adım at!",
        "Başarı yolculuğunda her gün yeni bir fırsat!",
        "Kendine inan, başaracaksın!"
    ]
}

async def get_food_suggestion(message: str) -> Dict[str, Any]:
    """Yemek önerisi döndürür"""
    for key in FOOD_DATABASE:
        if key in message.lower():
            return {
                "type": "food",
                "suggestions": FOOD_DATABASE[key],
                "message": "İşte size birkaç öneri:"
            }
    return {
        "type": "food",
        "suggestions": FOOD_DATABASE["akşam"],  # Varsayılan olarak akşam yemekleri
        "message": "Akşam için önerilerim:"
    }

async def get_coaching_message(message: str) -> Dict[str, Any]:
    """Motivasyon mesajı döndürür"""
    for key in COACHING_DATABASE:
        if key in message.lower():
            return {
                "type": "coaching",
                "message": COACHING_DATABASE[key][0],  # İlk motivasyon mesajını döndür
                "additional_messages": COACHING_DATABASE[key][1:]
            }
    return {
        "type": "coaching",
        "message": "Size nasıl yardımcı olabilirim?",
        "additional_messages": []
    }

@app.post("/chat")
async def chat(message: Message) -> Dict[str, Any]:
    """Ana chat endpoint'i"""
    try:
        # Mesajı analiz et ve uygun ajanı seç
        agent_response = await route_to_agent(message.text)
        selected_agent = agent_response["agent"]

        # Seçilen ajana göre yanıt oluştur
        if selected_agent == FOOD_AGENT:
            response = await get_food_suggestion(message.text)
        elif selected_agent == COACHING_AGENT:
            response = await get_coaching_message(message.text)
        else:
            raise HTTPException(status_code=400, detail="Bilinmeyen ajan tipi")

        return {
            "status": "success",
            "agent": selected_agent,
            "response": response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
