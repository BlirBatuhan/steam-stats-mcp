# Akıllı Ajan Router MCP

Bu proje, kullanıcı mesajlarını analiz ederek uygun ajanı seçen bir MCP (Message Control Protocol) servisidir.

## Özellikler

- Yemek önerileri için özel ajan
- Motivasyon ve koçluk için özel ajan
- FastAPI tabanlı HTTP API
- Smithery üzerinde deploy edilebilir

## Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı çalıştır
python app.py
```

## API Kullanımı

```bash
# Yemek önerisi al
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"text": "Akşam ne yesem?"}'

# Motivasyon mesajı al
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"text": "Bugün biraz moralsizim"}'
```

## Smithery Deployment

Bu proje Smithery üzerinde otomatik olarak deploy edilebilir. GitHub repository'sine push yapıldığında otomatik deployment tetiklenir.

## Lisans

MIT 