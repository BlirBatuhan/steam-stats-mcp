# Steam İstatistikleri MCP

[![smithery badge](https://smithery.ai/badge/@BlirBatuhan/steam-stats-mcp)](https://smithery.ai/server/@BlirBatuhan/steam-stats-mcp)

Bu proje, Steam'in en çok oynanan oyunlarının anlık oyuncu istatistiklerini gösteren bir MCP (Message Control Protocol) uygulamasıdır.

## Özellikler

- En çok oynanan 10 Steam oyununun listesi
- Her oyun için anlık oyuncu sayısı
- Oyuncu sayısına göre sıralama

## Kurulum

### Installing via Smithery

To install steam-stats-mcp for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@BlirBatuhan/steam-stats-mcp):

```bash
npx -y @smithery/cli install @BlirBatuhan/steam-stats-mcp --client claude
```

### Manual Installation
1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. `.env` dosyası oluşturun ve Steam API anahtarınızı ekleyin:
```
STEAM_API_KEY=your_api_key_here
```

## Kullanım

1. Sunucuyu başlatın:
```bash
python app.py
```

2. API'yi kullanın:
```bash
curl http://localhost:8000/top-games
```

## API Endpoint'leri

- `GET /top-games`: En çok oynanan Steam oyunlarını ve oyuncu sayılarını döndürür

## Örnek Yanıt

```json
{
  "status": "success",
  "games": [
    {
      "game_name": "Counter-Strike 2",
      "current_players": 1234567
    },
    {
      "game_name": "Dota 2",
      "current_players": 987654
    }
    // ... diğer oyunlar
  ]
}
``` 
