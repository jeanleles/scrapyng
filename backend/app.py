from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Configura a API do Gemini
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("API Key do Gemini não encontrada. Verifique o arquivo .env")
    genai.configure(api_key=gemini_api_key)
except Exception as e:
    print(f"Erro ao configurar a API do Gemini: {e}")


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

        for tag in body_content.find_all(['header', 'aside', 'footer', 'nav', 'script', 'style']):
            tag.decompose()

        # Filtra a palavra 'publicidade' de todas as tags extraídas
        headers_h1 = [text for h1 in body_content.find_all('h1') if (text := h1.get_text(strip=True)) and text.lower() != 'publicidade']
        headers_h2 = [text for h2 in body_content.find_all('h2') if (text := h2.get_text(strip=True)) and text.lower() != 'publicidade']
        headers_h3 = [text for h3 in body_content.find_all('h3') if (text := h3.get_text(strip=True)) and text.lower() != 'publicidade']
        headers_h4 = [text for h4 in body_content.find_all('h4') if (text := h4.get_text(strip=True)) and text.lower() != 'publicidade']
        headers_h5 = [text for h5 in body_content.find_all('h5') if (text := h5.get_text(strip=True)) and text.lower() != 'publicidade']
        headers_h6 = [text for h6 in body_content.find_all('h6') if (text := h6.get_text(strip=True)) and text.lower() != 'publicidade']
        spans = [text for span in body_content.find_all('span') if (text := span.get_text(strip=True)) and text.lower() != 'publicidade']
        blockquotes = [text for bq in body_content.find_all('blockquote') if (text := bq.get_text(strip=True)) and text.lower() != 'publicidade']
        divs = [text for div in body_content.find_all('div') if div.string and (text := div.get_text(strip=True)) and text.lower() != 'publicidade']
        paragraphs = [text for p in body_content.find_all('p') if (text := p.get_text(strip=True)) and text.lower() != 'publicidade']
        
        ul_lis = []
        for ul in body_content.find_all('ul'):
            ul_lis.extend([text for li in ul.find_all('li', recursive=False) if (text := li.get_text(strip=True)) and text.lower() != 'publicidade'])

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
        # 1. Scraping do conteúdo da página
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        body_content = soup.find('body')

        if not body_content:
            return jsonify({'error': 'Elemento <body> não encontrado na página.'}), 404
        
        for tag in body_content.find_all(['header', 'aside', 'footer', 'nav', 'script', 'style']):
            tag.decompose()

        texts = []
        for tag_name in ['h1','h2','h3','h4','h5','h6','p','span','blockquote','div', 'li']:
            elements = body_content.find_all(tag_name)
            for el in elements:
                text = el.get_text(strip=True)
                # Adiciona apenas texto que não seja vazio e não seja 'publicidade'
                if text and text.lower() != 'publicidade':
                    texts.append(text)
        
        full_text = '\n'.join(texts)

        if not full_text:
            return jsonify({'summary': 'Não foi possível extrair conteúdo textual da página para resumir.'})

        # 2. Geração do resumo com Gemini
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        prompt = f"Por favor, resuma o seguinte texto extraído de uma página da web em um ou dois parágrafos, em português do Brasil. Foque nos pontos mais importantes e ignore informações irrelevantes como menus ou textos de rodapé. O texto é:\n\n{full_text}"
        
        generation_config = genai.types.GenerationConfig(
            candidate_count=1,
            temperature=0.7,
        )

        gemini_response = model.generate_content(prompt, generation_config=generation_config)
        
        summary = gemini_response.text
        
        return jsonify({'summary': summary})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"Erro ao acessar a URL: {e}"}), 500
    except Exception as e:
        # Captura outros erros, incluindo os da API do Gemini
        print(f"Ocorreu um erro inesperado: {e}")
        return jsonify({'error': f"Erro ao gerar o resumo: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
