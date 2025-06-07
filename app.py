import os
import requests
from flask import Flask, request, jsonify, session, render_template_string

app = Flask(__name__)
app.secret_key = 'segr-condominio-smart-2024'

# Template HTML completo con tutto integrato
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEGR Condominio Smart</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f5f5; }
        .header { background: #D97835; color: white; padding: 1rem; display: flex; align-items: center; }
        .logo { width: 50px; height: 50px; background: white; border-radius: 50%; margin-right: 1rem; }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .chat-container { background: white; border-radius: 10px; padding: 2rem; margin-bottom: 2rem; }
        .chat-messages { height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 1rem; margin-bottom: 1rem; }
        .chat-input { width: 100%; padding: 1rem; border: 1px solid #ddd; border-radius: 5px; }
        .btn { background: #D97835; color: white; padding: 0.8rem 1.5rem; border: none; border-radius: 5px; cursor: pointer; }
        .btn:hover { background: #c56829; }
        .admin-section { background: white; border-radius: 10px; padding: 2rem; margin-top: 2rem; }
        .login-form { max-width: 300px; margin: 0 auto; }
        .form-group { margin-bottom: 1rem; }
        .form-control { width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 5px; }
        .dashboard { display: none; }
        .alert { padding: 1rem; margin: 1rem 0; border-radius: 5px; }
        .alert-success { background: #d4edda; color: #155724; }
        .alert-error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">SEGR</div>
        <h1>SEGR Condominio Smart - Assistente AI</h1>
    </div>

    <div class="container">
        <div class="chat-container">
            <h2>🤖 Assistente AI Condominio</h2>
            <div class="chat-messages" id="chatMessages">
                <div style="color: #666; font-style: italic;">
                    Ciao! Sono l'assistente AI del condominio. Puoi farmi domande su regolamenti, orari, spese e molto altro!
                </div>
            </div>
            <div style="display: flex; gap: 1rem;">
                <input type="text" class="chat-input" id="chatInput" placeholder="Scrivi la tua domanda...">
                <button class="btn" onclick="sendMessage()">Invia</button>
            </div>
        </div>

        <div class="admin-section">
            <div id="loginSection">
                <h3>🔐 Area Amministratore</h3>
                <div class="login-form">
                    <div class="form-group">
                        <input type="text" class="form-control" id="username" placeholder="Username">
                    </div>
                    <div class="form-group">
                        <input type="password" class="form-control" id="password" placeholder="Password">
                    </div>
                    <button class="btn" onclick="adminLogin()" style="width: 100%;">Accedi</button>
                </div>
            </div>

            <div id="dashboardSection" class="dashboard">
                <h3>📊 Dashboard Amministratore</h3>
                <div class="form-group">
                    <label>API Key DeepSeek:</label>
                    <input type="text" class="form-control" id="apiKey" placeholder="Inserisci API Key">
                    <button class="btn" onclick="saveApiKey()" style="margin-top: 0.5rem;">Salva API Key</button>
                </div>
                <div class="form-group">
                    <label>Nome Condominio:</label>
                    <input type="text" class="form-control" id="condominioName" placeholder="Nome del condominio">
                </div>
                <button class="btn" onclick="logout()">Logout</button>
            </div>
        </div>
    </div>

    <script>
        let isLoggedIn = false;
        let currentApiKey = '';

        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (!message) return;

            addMessageToChat('Tu: ' + message, 'user');
            input.value = '';

            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message, api_key: currentApiKey })
            })
            .then(response => response.json())
            .then(data => {
                addMessageToChat('🤖 AI: ' + data.response, 'ai');
            })
            .catch(error => {
                addMessageToChat('❌ Errore: ' + error.message, 'error');
            });
        }

        function addMessageToChat(message, type) {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.style.marginBottom = '10px';
            messageDiv.style.padding = '8px';
            messageDiv.style.borderRadius = '5px';
            
            if (type === 'user') {
                messageDiv.style.background = '#e3f2fd';
                messageDiv.style.textAlign = 'right';
            } else if (type === 'ai') {
                messageDiv.style.background = '#f1f8e9';
            } else {
                messageDiv.style.background = '#ffebee';
                messageDiv.style.color = '#c62828';
            }
            
            messageDiv.textContent = message;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function adminLogin() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            fetch('/admin/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('loginSection').style.display = 'none';
                    document.getElementById('dashboardSection').style.display = 'block';
                    isLoggedIn = true;
                } else {
                    alert('Credenziali non valide');
                }
            });
        }

        function saveApiKey() {
            const apiKey = document.getElementById('apiKey').value;
            currentApiKey = apiKey;
            
            fetch('/admin/save-api-key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ api_key: apiKey })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            });
        }

        function logout() {
            isLoggedIn = false;
            document.getElementById('loginSection').style.display = 'block';
            document.getElementById('dashboardSection').style.display = 'none';
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        }

        // Permetti invio con Enter
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    api_key = data.get('api_key', '')
    
    if not api_key:
        return jsonify({'response': 'Per favore configura l\'API key DeepSeek nell\'area amministratore.'})
    
    try:
        # Chiamata API DeepSeek
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': 'Sei un assistente AI per un condominio. Rispondi in italiano alle domande sui regolamenti condominiali, orari, spese e questioni amministrative.'},
                {'role': 'user', 'content': message}
            ],
            'max_tokens': 500,
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
            return jsonify({'response': f'Errore API: {response.status_code}'})
            
    except Exception as e:
        return jsonify({'response': f'Errore di connessione: {str(e)}'})

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    
    # Credenziali admin
    if username == 'admin' and password == 'admin123':
        session['admin_logged_in'] = True
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/admin/save-api-key', methods=['POST'])
def save_api_key():
    if not session.get('admin_logged_in'):
        return jsonify({'message': 'Non autorizzato'})
    
    data = request.json
    api_key = data.get('api_key', '')
    
    # Salva l'API key (in produzione usare database)
    os.environ['DEEPSEEK_API_KEY'] = api_key
    
    return jsonify({'message': 'API Key salvata con successo!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
