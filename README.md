# Scrapyng

#### by @jeanleles

#### Uma aplicação para fazer o scrap de páginas web, pegando os seus títulos (h1 e h2) e parágrafos (p). Caso você deseje ler os textos de uma página, mas não está sendo possível devido a algum modal, popup ou tarja que esteja na frente do conteúdo da página, tipo exigência de login, aceite de termos e cookies ou assinatura, você pode utilizar esta aplicação para obter o conteúdo da página apenas colocando a sua URL. Também é possível gerar um resumo do texto que foi extraído da página usaundo a ApyHub.

## 1. Tecnologias Utilizadas

- **Python**: Para o backend, usando Flask para criar a API que faz o scraping.
- **Flask**: Framework web para o backend em Python.
- **Beautiful Soup**: Biblioteca Python para extração de dados de arquivos HTML e XML.
- **Requests**: Biblioteca Python para fazer requisições HTTP.
- **Next.js 16**: Framework React utilizado no frontend com App Router.
- **Tailwind CSS**: Sistema de estilos utilizado para construir a interface responsiva.
- **Lucide React**: Biblioteca de ícones utilizada na interface.

## Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/jeanleles/scrapyng.git
cd scrapyng
```

### 2. Configuração do Backend

#### Instalar Dependências do Python

##### Acesse o diretório backend e instale todas as dependências necessárias:

```bash
cd backend
pip install -r requirements.txt
```

Copie `backend/.env.example` para `backend/.env` e preencha `GEMINI_API_KEY` quando quiser usar o resumo com IA.

No Windows, prepare um ambiente virtual e instale as dependências:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Para iniciar localmente no PowerShell:

```powershell
.\start-backend.ps1
```

No Linux/Docker, use `start-backend.sh`, que inicia o Gunicorn.

Para executar o backend localmente em modo de produção:

```bash
./start-backend.sh
```

O endpoint `GET /health` retorna `{"status":"ok"}` e pode ser usado por orquestradores para verificar a disponibilidade do serviço.

Para construir e executar apenas o container do backend:

```bash
docker build -t scrapyng-backend ./backend
docker run --rm -p 5555:5555 --env-file backend/.env scrapyng-backend
```

### 3. Configuração do Frontend

##### Acesse o diretório do frontend e instale as dependências do Next.js:

```bash
cd frontend
npm install
```

##### Para desenvolvimento, execute:

```bash
npm run dev
```

##### Para produção, gere o build e inicie o servidor:

```bash
npm run build
npm run start
```

O frontend estará disponível em `http://localhost:3000` no modo de desenvolvimento ou em `http://localhost:8080` usando o script `start-frontend.sh`. Configure `NEXT_PUBLIC_API_URL` em `frontend/.env.local` quando o backend não estiver em `http://localhost:5555`.

O frontend usa Next.js e não precisa mais de `http-server` ou PM2.

### 4. Deploy com Docker Compose e Caddy

No VPS, crie `backend/.env` a partir de `backend/.env.example` e preencha `GEMINI_API_KEY`. Em seguida, execute:

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f
```

O Compose publica o frontend apenas em `127.0.0.1:3000`; o backend não é publicado diretamente. Configure o Caddy para encaminhar o domínio para o frontend:

```caddyfile
scrapying.seudominio.com {
	reverse_proxy 127.0.0.1:3000
}
```

O frontend encaminha internamente `/api/scrape` e `/api/summarize` para o serviço backend. Assim, o navegador usa o mesmo domínio e não precisa conhecer o hostname interno do Docker.

Para atualizar a aplicação:

```bash
git pull
docker compose up -d --build
docker image prune -f
```

### 5. Utilização da Aplicação

#### 1. Acesse o frontend através do navegador em `http://localhost:3000` no modo de desenvolvimento ou `http://localhost:8080` quando iniciado pelo script de produção.

#### 2. Insira a URL da página que deseja fazer o scraping no campo de entrada.

#### 3. Clique no botão para obter os resultados.

#### 4. O conteúdo da página (tags h1, h2, p, etc.) será exibido logo abaixo.
