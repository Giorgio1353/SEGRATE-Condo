import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Leggi il contenuto di index.html
def get_html_content():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "<h1>Errore: File index.html non trovato</h1>"

@app.route('/')
def home():
    html_content = get_html_content()
    return html_content

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
