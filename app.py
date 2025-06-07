import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEGR Condominio Smart</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { background: #D97835; color: white; padding: 20px; text-align: center; border-radius: 10px; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; margin-top: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .chat-area { border: 2px solid #D97835; height: 400px; padding: 15px; margin: 20px 0; overflow-y: auto; background: #fafafa; border-radius: 8px; }
        .input-group { display: flex; gap: 10px; margin: 20px 0; }
        .input-group input { flex: 1; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }
        .btn { background: #D97835; color: white; padding: 12px 24px; border: none; cursor: pointer; border-radius: 5px; font-size: 16px; font-weight: bold; }
        .btn:hover { background: #c56829; }
        .message { margin-bottom: 15px; padding: 10px; border-radius: 8px; }
        .user-msg { background: #e3f2fd; text-align: right; }
        .ai-msg { background: #f1f8e9; }
        .config-section { background: #fff3e0; padding: 20px; border-radius: 8px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏢 SEGR Condominio Smart</h1>
        <p>Assistente AI per la Gestione Condominiale</p>
    </div>
    
    <div class="container">
        <h2>💬 Chat con l'Assistente AI</h2>
        <div class="chat-area" id="chatArea">
            <div class="message ai-msg">🤖 <strong>Assistente SEGR:</strong> Ciao! Sono l'assistente AI del condominio SEGR. Come posso aiutarti oggi?</div>
        </div>
        
        <div class="input-group">
            <input type="text" id="messageInput" placeholder="Scrivi la tua domanda sul condominio..." maxlength="500">
            <button class="btn" id="sendBtn">📤 Invia</button>
        </div>
        
        <div class="config-section">
            <h3>🔧 Configurazione API DeepSeek</h3>
            <div class="input-group">
                <input type="password" id="apiKeyInput" placeholder="Inserisci la tua API Key DeepSeek">
                <button class="btn" id="saveApiBtn">💾 Salva API</button>
            </div>
            <p style="color: #666; font-size: 14px;">
                ℹ️ <strong>Info:</strong> L'API Key viene salvata temporaneamente per questa sessione.<br>
                🌐 <strong>URL Sistema:</strong> https://condsegrate-93e925a52f32.herokuapp.com/
            </p>
        </div>
    </div>

    <script>
        let currentApiKey = localStorage.getItem('segr_api_key') || '';
        
        // Carica API key salvata
        if (currentApiKey) {
            document.getElementById('apiKeyInput').value = currentApiKey;
        }
        
        // Event listeners
        document.getElementById('sendBtn').addEventListener('click', sendMessage);
        document.getElementById('saveApiBtn').addEventListener('click', saveApiKey);
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) {
                alert('Scrivi un messaggio!');
                return;
            }
            
            if (!currentApiKey) {
                alert('Prima inserisci e salva l\'API Key DeepSeek!');
                return;
            }
            
            // Aggiungi messaggio utente
            addMessage('👤 <strong>Tu:</strong> ' + message, 'user-msg');
            input.value = '';
            
            // Disabilita pulsante durante invio
            const sendBtn = document.getElementById('sendBtn');
            sendBtn.disabled = true;
            sendBtn.textContent = '⏳ Invio...';
            
            // Chiamata API
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    api_key: currentApiKey
                })
            })
            .then(response => response.json())
            .then(data => {
                addMessage('🤖 <strong>Assistente SEGR:</strong> ' + data.response, 'ai-msg');
            })
            .catch(error => {
                addMessage('❌ <strong>Errore:</strong> ' + error.message, 'ai-msg');
            })
            .finally(() => {
                sendBtn.disabled = false;
                sendBtn.textContent = '📤 Invia';
            });
        }
        
        function addMessage(text, className) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + className;
            messageDiv.innerHTML = text;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function saveApiKey() {
            const apiKeyInput = document.getElementById('apiKeyInput');
            const apiKey = apiKeyInput.value.trim();
            
            if (!apiKey) {
                alert('Inserisci l\'API Key!');
                return;
            }
            
            currentApiKey = apiKey;
            localStorage.setItem('segr_api_key', apiKey);
            alert('✅ API Key salvata con successo!');
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.json
        message = data.get('message', '')
        api_key = data.get('api_key', '')
        
        if not message:
            return jsonify({'response': 'Messaggio vuoto ricevuto.'})
        
        if not api_key:
            return jsonify({'response': 'API Key mancante. Configurala nell\'area dedicata.'})
        
        # Chiamata a DeepSeek API
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'deepseek-chat',
            'messages': [
                {
                    'role': 'system', 
                    'content': 'Sei un assistente AI specializzato nella gestione condominiale. Rispondi sempre in italiano. Aiuti i condomini con domande su regolamenti, orari, spese condominiali, manutenzioni, assemblee e questioni amministrative. Sii cordiale e professionale.'
                },
                {
                    'role': 'user', 
                    'content': message
                }
            ],
            'max_tokens': 1000,
            'temperature': 0.7
        }
        
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            return jsonify({'response': ai_response})
        else:
            return jsonify({'response': f'Errore API DeepSeek (Codice: {response.status_code}). Verifica la tua API Key.'})
            
    except requests.exceptions.Timeout:
        return jsonify({'response': 'Timeout nella risposta. Riprova tra poco.'})
    except Exception as e:
        return jsonify({'response': f'Errore di sistema: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
