from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv
import google.generativeai as genai
from werkzeug.middleware.proxy_fix import ProxyFix
from safe_fetch import SafeFetchError, fetch_html

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
if os.getenv("TRUST_PROXY_HEADERS", "false").lower() == "true":
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=os.getenv("RATELIMIT_STORAGE_URI", "memory://"),
    default_limits=[],
)
MAX_GEMINI_CHARS = 100_000


def extract_summary_text(body_content):
    texts = []
    remaining_chars = MAX_GEMINI_CHARS
    for text in body_content.stripped_strings:
        if text.lower() == 'publicidade':
            continue
        if remaining_chars <= 0:
            break
        text = text[:remaining_chars]
        texts.append(text)
        remaining_chars -= len(text) + 1
    return '\n'.join(texts)

# Configura a API do Gemini
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("API Key do Gemini não encontrada. Verifique o arquivo .env")
    genai.configure(api_key=gemini_api_key)
except Exception as e:
    print(f"Erro ao configurar a API do Gemini: {e}")


@app.route('/scrape', methods=['POST'])
@limiter.limit(os.getenv("SCRAPE_RATE_LIMIT", "10 per minute"))
def scrape_content():
    if not request.is_json:
        return jsonify({'error': 'O conteúdo deve ser enviado como JSON.'}), 415
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Corpo JSON inválido.'}), 400
    url = data.get('url')
    if not isinstance(url, str) or not url:
        return jsonify({'error': 'URL é obrigatória'}), 400

    try:
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'html.parser')
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

    except SafeFetchError as error:
        return jsonify({'error': str(error)}), error.status_code

@app.route('/summarize', methods=['POST'])
@limiter.limit(os.getenv("SUMMARIZE_RATE_LIMIT", "3 per minute"))
def summarize_content():
    if not request.is_json:
        return jsonify({'error': 'O conteúdo deve ser enviado como JSON.'}), 415
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Corpo JSON inválido.'}), 400
    url = data.get('url')
    if not isinstance(url, str) or not url:
        return jsonify({'error': 'URL é obrigatória'}), 400
    
    try:
        # 1. Scraping do conteúdo da página
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        body_content = soup.find('body')

        if not body_content:
            return jsonify({'error': 'Elemento <body> não encontrado na página.'}), 404
        
        for tag in body_content.find_all(['header', 'aside', 'footer', 'nav', 'script', 'style']):
            tag.decompose()

        full_text = extract_summary_text(body_content)

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

    except SafeFetchError as error:
        return jsonify({'error': str(error)}), error.status_code
    except Exception as e:
        # Captura outros erros, incluindo os da API do Gemini
        print(f"Ocorreu um erro inesperado: {e}")
        return jsonify({'error': f"Erro ao gerar o resumo: {e}"}), 500

@app.get('/health')
def health_check():
    return jsonify({'status': 'ok'}), 200


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({'error': 'O corpo da requisição excede o limite permitido.'}), 413


@app.errorhandler(429)
def rate_limit_exceeded(_error):
    return jsonify({'error': 'Limite de requisições excedido. Tente novamente mais tarde.'}), 429


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5555'))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
