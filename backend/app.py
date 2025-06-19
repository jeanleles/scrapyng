from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

APYHUB_API_KEY = os.getenv('APYHUB_API_KEY', 'APY07HZwoVvly2KjXmxgQw65H2FUEgCGTGN8paxZXbYtVXkoYqWR45QnbKuYxMv0mkyD9vy')

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
        headers_h3 = [h3.get_text() for h3 in body_content.find_all('h3')]
        headers_h4 = [h4.get_text() for h4 in body_content.find_all('h4')]
        headers_h5 = [h5.get_text() for h5 in body_content.find_all('h5')]
        headers_h6 = [h6.get_text() for h6 in body_content.find_all('h6')]
        spans = [span.get_text() for span in body_content.find_all('span')]
        blockquotes = [bq.get_text() for bq in body_content.find_all('blockquote')]
        # Divs apenas com texto puro (sem tags filhas)
        divs = [div.get_text() for div in body_content.find_all('div') if div.string and div.string.strip()]
        # ul > li
        ul_lis = []
        for ul in body_content.find_all('ul'):
            ul_lis.extend([li.get_text() for li in ul.find_all('li', recursive=False)])
        paragraphs = [p.get_text() for p in body_content.find_all('p')]

        result = {
            'h1': headers_h1,
            'h2': headers_h2,
            'h3': headers_h3,
            'h4': headers_h4,
            'h5': headers_h5,
            'h6': headers_h6,
            'p': paragraphs,
            'span': spans,
            'blockquote': blockquotes,
            'div': divs,
            'ul_li': ul_lis
        }

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize_content():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL é obrigatória'}), 400
    try:
        # Reutiliza a lógica de scraping
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        body_content = soup.find('body')
        if not body_content:
            return jsonify({'error': 'Elemento <body> não encontrado na página.'}), 404
        for tag in body_content.find_all(['header', 'aside', 'footer']):
            tag.decompose()
        # Coleta textos das principais tags
        texts = []
        for tag in ['h1','h2','h3','h4','h5','h6','p','span','blockquote','div']:
            if tag == 'div':
                texts.extend([div.get_text() for div in body_content.find_all('div') if div.string and div.string.strip()])
            else:
                texts.extend([el.get_text() for el in body_content.find_all(tag)])
        # ul > li
        for ul in body_content.find_all('ul'):
            texts.extend([li.get_text() for li in ul.find_all('li', recursive=False)])
        # Junta tudo em um texto só
        full_text = '\n'.join([t.strip() for t in texts if t.strip()])
        # Chama a API da ApyHub
        apyhub_url = 'https://api.apyhub.com/ai/summarize-text'
        payload = {
            'text': full_text,
            'summary_length': 'medium',
            'output_language': 'pt_BR'
        }
        headers = {
            'Content-Type': 'application/json',
            'apy-token': APYHUB_API_KEY
        }
        api_response = requests.post(apyhub_url, json=payload, headers=headers)
        if api_response.status_code != 200:
            msg = 'Resumo não pôde ser gerado devido ao limite de chamadas da API gratuita ou instabilidade do serviço. Tente novamente mais tarde.'
            return jsonify({'summary': msg, 'fallback': True}), 200
        summary = api_response.json().get('data', {}).get('summary', '')
        return jsonify({'summary': summary})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='172.21.2.152', port=5555, debug=True) # 172.21.2.152 - IP da minha VM Ubuntu no WSL
