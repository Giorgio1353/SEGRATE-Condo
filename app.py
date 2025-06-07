from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html>
<head><title>SEGR Test</title></head>
<body>
<h1>SEGR Condominio Smart</h1>
<p>Sistema funzionante!</p>
<p>URL: https://condsegrate-93e925a52f32.herokuapp.com/</p>
</body>
</html>'''

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
