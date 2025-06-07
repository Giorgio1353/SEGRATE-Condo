import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
app.secret_key = 'segr-key-2024'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEGR Condominio Smart</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { background: #D97835; color: white; padding: 20px; text-align: center; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; margin-top: 20px; }
        .chat-area { border: 1px solid #ddd; height: 300px; padding: 15px; margin: 20px 0; overflow-y: auto; }
        .input-group { display: flex; gap: 10px; margin: 10px 0; }
        .input-group input { flex: 1; padding: 10px; border: 1px solid #ddd; }
        .btn { background: #D97835; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .btn:hover { background: #c56829; }
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
            <div style="color: #666;">Ciao! Sono l'assistente AI del condominio SEGR. Come posso aiutarti?</div>
        </div>
        
        <div class="input-group">
            <input type="text" id="messageInput" placeholder="Scrivi la tua domanda..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button class="btn" onclick="sendMessage()">Invia</button>
        </div>
        
        <hr style="margin: 30px 0;">
        
        <h3>🔧 Configurazione Admin</h3>
        <div class="input-group">
            <input type="password" id="apiKey" placeholder="API Key DeepSeek">
            <button class="btn" onclick="saveApiKey()">Salva API</button>
        </div>
        
        <p><strong>Credenziali Admin:</strong> admin / admin123</p>
        <p><strong>URL Sistema:</strong> <a href="https://condsegrate-93e925a52f32.herokuapp.com/">https://condsegrate-93e925a52f32.herokuapp.com/</a></p>
    </div>

    <script>
        let apiKey = '';
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage('👤 Tu: ' + message);
            input.value = '';
            
            if (!apiKey) {
                addMessage('🤖 AI: Per favore inserisci l\'API Key DeepSeek nella configurazione.');
                return;
            }
            
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message, api_key: apiKey})
            })
            .then(response => response.json())
            .then(data => addMessage('🤖 AI: ' + data.response))
            .catch(error => addMessage('❌ Errore: ' + error.message));
        }
        
        function addMessage(text) {
            const chatArea = document.getElementById('chatArea');
            const div = document.createElement('div');
            div.style.marginBottom = '10px';
            div.style.padding = '8px';
            div.style.background = text.includes('👤') ? '#e3f2fd' : '#f1f8e9';
            div.textContent = text;
            chatArea.appendChild(div);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function saveApiKey() {
            const key = document.getElementById('apiKey').value;
            apiKey = key;
            alert('API Key salvata!');
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        return jsonify({'response': f'Ricevuto: {message}. Sistema SEGR attivo!'})
    except Exception as e:
        return jsonify({'response': f'Errore: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
