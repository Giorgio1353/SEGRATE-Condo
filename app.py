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
