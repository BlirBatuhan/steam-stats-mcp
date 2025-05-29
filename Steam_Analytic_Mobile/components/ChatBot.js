import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, Alert, Platform } from 'react-native';

// Steam agent URL'sini platforma göre ayarla
const STEAM_AGENT_URL = Platform.select({
  android: 'http://10.0.2.2:4111/api', // Android Emulator için
  ios: 'http://localhost:4111/api', // iOS Simulator için
  default: 'http://localhost:4111/api'
});

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);

  useEffect(() => {
    // Steam agent'a bağlanma
    connectToSteamAgent();
  }, []);

  const connectToSteamAgent = async () => {
    if (isConnecting) return;
    
    setIsConnecting(true);
    try {
      console.log('Steam agent\'a bağlanılıyor...', STEAM_AGENT_URL);
      
      // Zaman aşımı süresini 60 saniyeye çıkaralım
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 saniye zaman aşımı

      // Önce bir test isteği gönderelim
      const testResponse = await fetch(`${STEAM_AGENT_URL}/health`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        signal: controller.signal
      }).catch(error => {
        console.error('Test isteği hatası:', error);
        throw new Error('Steam agent erişilemez durumda: ' + error.message);
      });

      if (!testResponse.ok) {
        throw new Error('Steam agent erişilemez durumda: ' + testResponse.status);
      }

      const response = await fetch(`${STEAM_AGENT_URL}/agents/steamAgent/connect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        signal: controller.signal
      }).catch(error => {
        console.error('Bağlantı isteği hatası:', error);
        throw new Error('Bağlantı isteği başarısız: ' + error.message);
      });

      clearTimeout(timeoutId);
      console.log('Bağlantı yanıtı:', response.status);
      
      if (response.ok) {
        setIsConnected(true);
        addBotMessage('Steam Analytics asistanına bağlandım. Size nasıl yardımcı olabilirim?');
      } else {
        const errorText = await response.text();
        console.error('Bağlantı hatası:', response.status, errorText);
        addBotMessage('Steam Analytics asistanına bağlanırken bir hata oluştu. Lütfen daha sonra tekrar deneyin.');
        Alert.alert(
          'Bağlantı Hatası',
          `Steam agent'a bağlanılamadı. (${response.status})\nLütfen Steam agent'ın çalıştığından emin olun.`
        );
      }
    } catch (error) {
      console.error('Bağlantı hatası:', error);
      if (error.name === 'AbortError') {
        addBotMessage('Bağlantı zaman aşımına uğradı. Lütfen Steam agent\'ın çalıştığından emin olun.');
        Alert.alert(
          'Bağlantı Hatası',
          'Bağlantı zaman aşımına uğradı. Lütfen Steam agent\'ın çalıştığından emin olun.'
        );
      } else {
        addBotMessage('Bağlantı hatası oluştu. Lütfen daha sonra tekrar deneyin.');
        Alert.alert(
          'Bağlantı Hatası',
          `Steam agent'a bağlanılamadı: ${error.message}\nLütfen Steam agent'ın çalıştığından emin olun.`
        );
      }
    } finally {
      setIsConnecting(false);
    }
  };

  const addBotMessage = (text) => {
    const botMessage = {
      text,
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages(prevMessages => [...prevMessages, botMessage]);
  };

  const handleSend = async () => {
    if (inputText.trim() === '') return;

    // Kullanıcı mesajını ekle
    const userMessage = {
      text: inputText,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages([...messages, userMessage]);
    setInputText('');

    if (!isConnected) {
      addBotMessage('Steam Analytics asistanına bağlı değilim. Lütfen bağlantıyı kontrol edin.');
      Alert.alert(
        'Bağlantı Hatası',
        'Steam agent\'a bağlı değilsiniz. Yeniden bağlanmayı deneyin.'
      );
      return;
    }

    try {
      console.log('Mesaj gönderiliyor:', inputText);
      // Steam agent'a mesaj gönder
      const response = await fetch(`${STEAM_AGENT_URL}/agents/steamAgent/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ 
          message: inputText,
          stream: false
        }),
      }).catch(error => {
        console.error('Mesaj gönderme hatası:', error);
        throw new Error('Mesaj gönderme isteği başarısız: ' + error.message);
      });

      console.log('Mesaj yanıtı:', response.status);

      if (response.ok) {
        const data = await response.json();
        console.log('Steam agent yanıtı:', data);

        // Steam agent'ın yanıtını kontrol et
        if (data && data.content) {
          addBotMessage(data.content);
        } else if (data && data.response) {
          addBotMessage(data.response);
        } else if (data && data.message) {
          addBotMessage(data.message);
        } else {
          console.error('Beklenmeyen yanıt formatı:', data);
          addBotMessage('Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.');
        }
      } else {
        const errorData = await response.text();
        console.error('HTTP Hatası:', response.status, errorData);
        addBotMessage('Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.');
        Alert.alert(
          'Hata',
          'Mesaj gönderilirken bir hata oluştu. Lütfen tekrar deneyin.'
        );
      }
    } catch (error) {
      console.error('Mesaj gönderme hatası:', error);
      addBotMessage('Mesaj gönderilirken bir hata oluştu. Lütfen tekrar deneyin.');
      Alert.alert(
        'Hata',
        `Mesaj gönderilirken bir hata oluştu: ${error.message}\nLütfen tekrar deneyin.`
      );
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.statusBar}>
        <Text style={[styles.statusText, isConnected ? styles.connected : styles.disconnected]}>
          {isConnecting ? 'Bağlanıyor...' : isConnected ? 'Bağlı' : 'Bağlantı Kesik'}
        </Text>
        {!isConnected && !isConnecting && (
          <TouchableOpacity style={styles.retryButton} onPress={connectToSteamAgent}>
            <Text style={styles.retryButtonText}>Yeniden Dene</Text>
          </TouchableOpacity>
        )}
      </View>
      <ScrollView style={styles.messagesContainer}>
        {messages.map((message, index) => (
          <View
            key={index}
            style={[
              styles.messageBubble,
              message.sender === 'user' ? styles.userMessage : styles.botMessage,
            ]}
          >
            <Text style={[
              styles.messageText,
              message.sender === 'bot' ? styles.botMessageText : styles.userMessageText
            ]}>
              {message.text}
            </Text>
            <Text style={[
              styles.timestamp,
              message.sender === 'bot' ? styles.botTimestamp : styles.userTimestamp
            ]}>
              {message.timestamp}
            </Text>
          </View>
        ))}
      </ScrollView>
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Mesajınızı yazın..."
          placeholderTextColor="#999"
        />
        <TouchableOpacity 
          style={[styles.sendButton, !isConnected && styles.sendButtonDisabled]} 
          onPress={handleSend}
          disabled={!isConnected}
        >
          <Text style={styles.sendButtonText}>Gönder</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1b2838',
  },
  statusBar: {
    padding: 5,
    backgroundColor: '#171a21',
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
  },
  statusText: {
    fontSize: 12,
    fontWeight: 'bold',
    marginRight: 10,
  },
  connected: {
    color: '#66c0f4',
  },
  disconnected: {
    color: '#ff6b6b',
  },
  retryButton: {
    backgroundColor: '#66c0f4',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 5,
  },
  retryButtonText: {
    color: '#ffffff',
    fontSize: 12,
  },
  messagesContainer: {
    flex: 1,
    padding: 10,
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 10,
    borderRadius: 10,
    marginVertical: 5,
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#66c0f4',
  },
  botMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#2a475e',
  },
  messageText: {
    fontSize: 16,
  },
  userMessageText: {
    color: '#ffffff',
  },
  botMessageText: {
    color: '#ffffff',
  },
  timestamp: {
    fontSize: 12,
    marginTop: 5,
  },
  userTimestamp: {
    color: 'rgba(255,255,255,0.7)',
  },
  botTimestamp: {
    color: 'rgba(255,255,255,0.7)',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 10,
    backgroundColor: '#171a21',
    borderTopWidth: 1,
    borderTopColor: '#2a475e',
  },
  input: {
    flex: 1,
    backgroundColor: '#2a475e',
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 8,
    marginRight: 10,
    fontSize: 16,
    color: '#ffffff',
  },
  sendButton: {
    backgroundColor: '#66c0f4',
    borderRadius: 20,
    paddingHorizontal: 20,
    justifyContent: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#4a5568',
  },
  sendButtonText: {
    color: '#ffffff',
    fontSize: 16,
  },
});

export default ChatBot; 