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
        input[type="submit"]:hover {{ background: #c56829; }}
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
            <p>Assistente AI per la Gestione Condominiale</p>
            <p style="font-size: 14px;">Powered by Anthropic Claude</p>
        </div>
        
        <div class="status">
            <strong>Status API Anthropic:</strong> {api_status}<br>
            <strong>API Key:</strong> {api_display}<br>
            <strong>Modello:</strong> Claude-3 Sonnet<br>
            <strong>URL Sistema:</strong> https://condsegrate-93e925a52f32.herokuapp.com/
        </div>
        
        <h3>💬 Chat con Assistente AI Claude</h3>
        <div class="chat">
            {messages_html}
        </div>
        
        <form method="POST" action="/send">
            <div class="form-row">
                <input type="text" name="message" placeholder="Scrivi la tua domanda sul condominio..." required maxlength="400">
                <input type="submit" value="📤 INVIA MESSAGGIO">
            </div>
        </form>
        
        <hr style="margin: 30px 0;">
        
        <h3>🔑 Configurazione API Anthropic</h3>
        <form method="POST" action="/save_api">
            <div class="form-row">
                <input type="password" name="api_key" placeholder="API Key Anthropic (sk-ant-...)" value="">
                <input type="submit" value="💾 SALVA API KEY">
            </div>
        </form>
        
        <p style="color: #666; font-size: 14px;">
            💡 <strong>Istruzioni:</strong><br>
            1. Ottieni API Key da: <a href="https://console.anthropic.com/" target="_blank">console.anthropic.com</a><br>
            2. Inserisci la chiave che inizia con "sk-ant-..." e clicca SALVA<br>
            3. Scrivi una domanda e clicca INVIA MESSAGGIO<br>
            4. Claude AI ti risponderà in italiano!<br><br>
            🎯 <strong>Esempi domande:</strong> "Orari silenzio", "Spese condominiali", "Regolamento ascensore"
        </p>
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
        messages.append("❌ <strong>Sistema:</strong> Prima configura l'API Key Anthropic!")
        return redirect('/')
    
    try:
    # Anthropic Claude API - Versione semplificata
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01'
    }
    
    # Payload semplificato
    payload = {
        'model': 'claude-3-haiku-20240307',
        'max_tokens': 500,
        'messages': [
            {
                'role': 'user',
                'content': f"Rispondi in italiano: {message}"
            }
        ]
    }
    
    response = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers=headers, 
        json=payload, 
        timeout=20
    )
    
    print(f"Status: {response.status_code}")  # Debug
    print(f"Response: {response.text}")       # Debug
    
    if response.status_code == 200:
        result = response.json()
        ai_response = result['content'][0]['text']
        messages.append(f"🤖 <strong>Claude AI:</strong> {ai_response}")
    else:
        messages.append(f"❌ <strong>Debug:</strong> Status {response.status_code} - {response.text[:100]}")
        
except Exception as e:
    messages.append(f"❌ <strong>Errore:</strong> {str(e)}")        
    
    # Mantieni solo gli ultimi 20 messaggi
    if len(messages) > 20:
        messages = messages[-20:]
    
    return redirect('/')

@app.route('/save_api', methods=['POST'])
def save_api():
    global api_key, messages
    
    new_key = request.form.get('api_key', '').strip()
    
    if new_key:
        if new_key.startswith('sk-ant-'):
            api_key = new_key
            messages.append("✅ <strong>Sistema:</strong> API Key Anthropic salvata con successo!")
        else:
            messages.append("❌ <strong>Errore:</strong> API Key non valida. Deve iniziare con 'sk-ant-'")
    else:
        messages.append("❌ <strong>Sistema:</strong> API Key vuota!")
    
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
