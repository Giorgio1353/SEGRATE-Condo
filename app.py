from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)

# Variabili globali
api_key = ""
messages = ["🤖 Sistema SEGR attivo! Inserisci API key Anthropic e fai una domanda."]

def get_html():
    api_status = "Configurata ✅" if api_key else "Non configurata ❌"
    api_display = api_key[:15] + "..." if api_key else ""
    
    messages_html = ""
    for msg in messages:
        css_class = "user" if "👤" in msg else "ai"
        messages_html += f'<div class="msg {css_class}">{msg}</div>'
    
    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>SEGR Condominio Smart</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial; padding: 20px; background: #f0f0f0; }}
        .container {{ max-width: 700px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
        .header {{ background: #D97835; color: white; padding: 20px; text-align: center; margin: -30px -30px 30px -30px; border-radius: 10px 10px 0 0; }}
        .chat {{ border: 2px solid #D97835; height: 350px; padding: 15px; overflow-y: scroll; margin: 20px 0; background: #fafafa; }}
        .form-row {{ margin: 15px 0; }}
        input[type="text"] {{ width: 75%; padding: 12px; border: 2px solid #ddd; font-size: 16px; }}
        input[type="password"] {{ width: 75%; padding: 12px; border: 2px solid #ddd; font-size: 16px; }}
        input[type="submit"] {{ padding: 12px 25px; background: #D97835; color: white; border: none; cursor: pointer; font-size: 16px; font-weight: bold; }}
        .msg {{ margin: 8px 0; padding: 12px; border-radius: 8px; }}
        .user {{ background: #e3f2fd; border-left: 4px solid #2196F3; }}
        .ai {{ background: #f1f8e9; border-left: 4px solid #4CAF50; }}
        .status {{ background: #fff3e0; padding: 15px; border-radius: 5px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 SEGR Condominio Smart</h1>
            <p>Assistente AI Claude</p>
        </div>
        
        <div class="status">
            <strong>API Status:</strong> {api_status}<br>
            <strong>URL:</strong> https://condsegrate-93e925a52f32.herokuapp.com/
        </div>
        
        <h3>💬 Chat AI</h3>
        <div class="chat">
            {messages_html}
        </div>
        
        <form method="POST" action="/send">
            <div class="form-row">
                <input type="text" name="message" placeholder="Domanda..." required>
                <input type="submit" value="📤 INVIA">
            </div>
        </form>
        
        <hr>
        
        <h3>🔑 API Anthropic</h3>
        <form method="POST" action="/save_api">
            <div class="form-row">
                <input type="password" name="api_key" placeholder="sk-ant-...">
                <input type="submit" value="💾 SALVA">
            </div>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return get_html()

@app.route('/send', methods=['POST'])
def send_message():
    global messages
    
    message = request.form.get('message', '').strip()
    if not message:
        return redirect('/')
    
    messages.append(f"👤 <strong>Tu:</strong> {message}")
    
    if not api_key:
        messages.append("❌ API Key mancante!")
        return redirect('/')
    
    try:
        headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            'model': 'claude-3-haiku-20240307',
            'max_tokens': 400,
            'messages': [{'role': 'user', 'content': message}]
        }
        
        response = requests.post('https://api.anthropic.com/v1/messages', 
                               headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['content'][0]['text']
            messages.append(f"🤖 <strong>Claude:</strong> {ai_response}")
        else:
            messages.append(f"❌ Errore: {response.status_code}")
            
    except Exception as e:
        messages.append(f"❌ Errore: {str(e)}")
    
    if len(messages) > 15:
        messages = messages[-15:]
    
    return redirect('/')

@app.route('/save_api', methods=['POST'])
def save_api():
    global api_key, messages
    
    new_key = request.form.get('api_key', '').strip()
    if new_key:
        api_key = new_key
        messages.append("✅ API Key salvata!")
    
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
