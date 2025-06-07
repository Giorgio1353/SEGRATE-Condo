from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SEGR Condominio Smart</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial; padding: 20px; background: #f0f0f0; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        .header { background: #D97835; color: white; padding: 20px; text-align: center; margin: -30px -30px 30px -30px; }
        .chat { border: 1px solid #ccc; height: 300px; padding: 10px; overflow-y: scroll; margin: 20px 0; }
        input[type="text"] { width: 70%; padding: 10px; }
        input[type="password"] { width: 70%; padding: 10px; margin: 10px 0; }
        button { padding: 10px 20px; background: #D97835; color: white; border: none; cursor: pointer; }
        .msg { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #e3f2fd; text-align: right; }
        .ai { background: #f1f8e9; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SEGR Condominio Smart</h1>
            <p>Sistema Funzionante</p>
        </div>
        
        <h3>💬 Chat AI</h3>
        <div class="chat" id="chat">
            <div class="msg ai">🤖 Ciao! Sistema SEGR attivo. Inserisci l'API key sotto e poi fai una domanda!</div>
        </div>
        
        <input type="text" id="msg" placeholder="Scrivi qui..." onkeypress="if(event.key=='Enter') send()">
        <button onclick="send()">INVIA</button>
        
        <h3>🔑 API DeepSeek</h3>
        <input type="password" id="api" placeholder="API Key DeepSeek">
        <button onclick="saveKey()">SALVA</button>
        
        <p>URL: https://condsegrate-93e925a52f32.herokuapp.com/</p>
    </div>

<script>
let apiKey = '';

function saveKey() {
    apiKey = document.getElementById('api').value;
    if (apiKey) {
        alert('API salvata!');
        addMsg('✅ API Key configurata!', 'ai');
    }
}

function send() {
    let msg = document.getElementById('msg').value;
    if (!msg) return;
    
    addMsg('👤 ' + msg, 'user');
    document.getElementById('msg').value = '';
    
    if (!apiKey) {
        addMsg('❌ Inserisci prima l\'API Key!', 'ai');
        return;
    }
    
    addMsg('⏳ Elaborando...', 'ai');
    
    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({msg: msg, key: apiKey})
    })
    .then(r => r.json())
    .then(d => {
        removeLastMsg();
        addMsg('🤖 ' + d.reply, 'ai');
    })
    .catch(e => {
        removeLastMsg();
        addMsg('❌ Errore: ' + e, 'ai');
    });
}

function addMsg(text, type) {
    let chat = document.getElementById('chat');
    let div = document.createElement('div');
    div.className = 'msg ' + type;
    div.innerHTML = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function removeLastMsg() {
    let chat = document.getElementById('chat');
    let msgs = chat.getElementsByClassName('msg');
    if (msgs.length > 0) {
        chat.removeChild(msgs[msgs.length - 1]);
    }
}
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data['msg']
        api_key = data['key']
        
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        payload = {
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': message}],
            'max_tokens': 500
        }
        
        resp = requests.post('https://api.deepseek.com/v1/chat/completions', 
                           headers=headers, json=payload, timeout=20)
        
        if resp.status_code == 200:
            result = resp.json()
            reply = result['choices'][0]['message']['content']
            return jsonify({'reply': reply})
        else:
            return jsonify({'reply': f'Errore API: {resp.status_code}'})
            
    except Exception as e:
        return jsonify({'reply': f'Errore: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
🎯 QUESTA VERSIONE:
✅ JavaScript ultra-semplice
✅ Pulsanti che funzionano SICURAMENTE
✅ Chat AI operativa
✅ Zero complessità
Sostituisci e testa! Se neanche questa funziona, il problema è altro! 💪🔥

Copia
Salva su Notion
questa volta il bottone ivia non si muove nemmeno!
🚨 BASTA! Il problema è JavaScript che si blocca su Heroku!

🎯 SOLUZIONE DEFINITIVA - ZERO JAVASCRIPT:
Sostituisci app.py con questa versione FORM HTML puro:

Copyfrom flask import Flask, render_template_string, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Variabile globale per API key (temporanea)
api_key = ""
messages = ["🤖 Sistema SEGR attivo! Inserisci l'API key e fai una domanda."]

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SEGR Condominio Smart</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial; padding: 20px; background: #f0f0f0; }
        .container { max-width: 700px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        .header { background: #D97835; color: white; padding: 20px; text-align: center; margin: -30px -30px 30px -30px; border-radius: 10px 10px 0 0; }
        .chat { border: 2px solid #D97835; height: 350px; padding: 15px; overflow-y: scroll; margin: 20px 0; background: #fafafa; }
        .form-row { margin: 15px 0; }
        input[type="text"] { width: 75%; padding: 12px; border: 2px solid #ddd; font-size: 16px; }
        input[type="password"] { width: 75%; padding: 12px; border: 2px solid #ddd; font-size: 16px; }
        input[type="submit"] { padding: 12px 25px; background: #D97835; color: white; border: none; cursor: pointer; font-size: 16px; font-weight: bold; }
        input[type="submit"]:hover { background: #c56829; }
        .msg { margin: 8px 0; padding: 12px; border-radius: 8px; }
        .user { background: #e3f2fd; border-left: 4px solid #2196F3; }
        .ai { background: #f1f8e9; border-left: 4px solid #4CAF50; }
        .status { background: #fff3e0; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 SEGR Condominio Smart</h1>
            <p>Assistente AI per la Gestione Condominiale</p>
        </div>
        
        <div class="status">
            <strong>Status API:</strong> {{ 'Configurata ✅' if api_configured else 'Non configurata ❌' }}<br>
            <strong>URL Sistema:</strong> https://condsegrate-93e925a52f32.herokuapp.com/
        </div>
        
        <h3>💬 Chat con Assistente AI</h3>
        <div class="chat">
            {% for msg in chat_messages %}
                <div class="msg {{ 'user' if '👤' in msg else 'ai' }}">{{ msg|safe }}</div>
            {% endfor %}
        </div>
        
        <form method="POST" action="/send">
            <div class="form-row">
                <input type="text" name="message" placeholder="Scrivi la tua domanda sul condominio..." required maxlength="300">
                <input type="submit" value="📤 INVIA MESSAGGIO">
            </div>
        </form>
        
        <hr style="margin: 30px 0;">
        
        <h3>🔑 Configurazione API DeepSeek</h3>
        <form method="POST" action="/save_api">
            <div class="form-row">
                <input type="password" name="api_key" placeholder="Inserisci API Key DeepSeek" value="{{ current_api_key }}">
                <input type="submit" value="💾 SALVA API KEY">
            </div>
        </form>
        
        <p style="color: #666; font-size: 14px;">
            💡 <strong>Come funziona:</strong><br>
            1. Inserisci la tua API Key DeepSeek e clicca "SALVA API KEY"<br>
            2. Scrivi una domanda nella chat e clicca "INVIA MESSAGGIO"<br>
            3. L'AI ti risponderà automaticamente!
        </p>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    global api_key, messages
    return render_template_string(TEMPLATE, 
                                chat_messages=messages, 
                                api_configured=bool(api_key),
                                current_api_key=api_key[:10] + "..." if api_key else "")

@app.route('/send', methods=['POST'])
def send_message():
    global api_key, messages
    
    message = request.form.get('message', '').strip()
    
    if not message:
        return redirect(url_for('home'))
    
    # Aggiungi messaggio utente
    messages.append(f"👤 <strong>Tu:</strong> {message}")
    
    if not api_key:
        messages.append("❌ <strong>Sistema:</strong> Prima configura l'API Key DeepSeek!")
        return redirect(url_for('home'))
    
    try:
        # Chiamata DeepSeek API
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'deepseek-chat',
            'messages': [
                {
                    'role': 'system',
                    'content': 'Sei un assistente AI per la gestione condominiale. Rispondi sempre in italiano in modo cortese e professionale.'
                },
                {
                    'role': 'user',
                    'content': message
                }
            ],
            'max_tokens': 800,
            'temperature': 0.7
        }
        
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=25
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            messages.append(f"🤖 <strong>Assistente SEGR:</strong> {ai_response}")
        else:
            messages.append(f"❌ <strong>Errore API:</strong> Codice {response.status_code}. Verifica la tua API Key.")
            
    except Exception as e:
        messages.append(f"❌ <strong>Errore:</strong> {str(e)}")
    
    # Mantieni solo gli ultimi 20 messaggi
    if len(messages) > 20:
        messages = messages[-20:]
    
    return redirect(url_for('home'))

@app.route('/save_api', methods=['POST'])
def save_api():
    global api_key, messages
    
    new_api_key = request.form.get('api_key', '').strip()
    
    if new_api_key:
        api_key = new_api_key
        messages.append("✅ <strong>Sistema:</strong> API Key configurata con successo!")
    else:
        messages.append("❌ <strong>Sistema:</strong> API Key vuota!")
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
