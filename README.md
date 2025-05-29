# Steam Statistics MCP

Bu proje, Steam'in en popüler oyunlarının gerçek zamanlı oyuncu istatistiklerini sunan bir Model Context Protocol (MCP) sunucusudur. Kullanıcılar, en çok oynanan oyunları, oyuncu sayılarını ve oyun türlerini kolayca görüntüleyebilir.

## Özellikler
- Steam API üzerinden gerçek zamanlı oyuncu verisi
- En popüler oyunların listesi
- Oyun türlerine göre filtreleme
- Kullanıcıya özel son oynanan oyun ve istatistikler

## Kurulum ve Deploy

### 1. Gerekli Dosyalar
Aşağıdaki dosyalar MCP klasöründe bulunmalıdır:
- `server.py`
- `smithery.yaml`
- `Dockerfile`
- `requirements.txt`

### 2. Smithery ile Deploy Etme
1. **GitHub repository'sini Smithery'ye bağla.**
2. **Base Directory** olarak `MCP` yaz.
3. **Environment Variables** kısmına Steam API anahtarını ekle:
   - Key: `STEAM_API_KEY`
   - Value: `senin_steam_api_anahtarin`
4. Deploy işlemini başlat.

### 3. Lokal Çalıştırma
```bash
pip install -r requirements.txt
python server.py
```

## API Kullanımı
Smithery üzerinden deploy ettikten sonra, size verilen endpoint ile aşağıdaki fonksiyonları kullanabilirsiniz:
- En popüler oyunları listele
- Oyun türlerini sorgula
- Kullanıcıya özel istatistik çek

## Geliştirici Notları
- API anahtarınızı `.env` dosyasında veya platformun environment ayarlarında saklayın.
- Güvenlik için `.env` dosyasını asla repoya push etmeyin.

## Lisans
MIT 

## Smithery Sunucu Linki
- [Steam Statistics MCP](https://smithery.ai/server/@BlirBatuhan/steam-stats-mcp) 