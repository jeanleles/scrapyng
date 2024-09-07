from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

@app.route('/scrape', methods=['POST'])
def scrape_content():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL é obrigatória'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        body_content = soup.find('body')

        if not body_content:
            return jsonify({'error': 'Elemento <body> não encontrado na página.'}), 404

        for tag in body_content.find_all(['header', 'aside', 'footer']):
            tag.decompose()

        headers_h1 = [h1.get_text() for h1 in body_content.find_all('h1')]
        headers_h2 = [h2.get_text() for h2 in body_content.find_all('h2')]
        paragraphs = [p.get_text() for p in body_content.find_all('p')]

        result = {
            'h1': headers_h1,
            'h2': headers_h2,
            'p': paragraphs
        }

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='172.20.70.254', port=5555, debug=True) # 172.20.70.254 - IP da minha VM Ubuntu no WSL
