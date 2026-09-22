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

##### Acesse o diretório backend e instale as dependências necessárias:

```bash
cd backend
pip install flask beautifulsoup4 requests
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

O frontend usa Next.js e não precisa mais de `http-server` ou PM2. Em um ambiente Docker, o Docker Compose será responsável pela execução e reinicialização dos serviços.

### 4. Utilização da Aplicação

#### 1. Acesse o frontend através do navegador usando o endereço fornecido pelo http-server, por exemplo, http://localhost:8080.

#### 2. Insira a URL da página que deseja fazer o scraping no campo de entrada.

#### 3. Clique no botão para obter os resultados.

#### 4. O conteúdo da página (tags h1, h2, p, etc.) será exibido logo abaixo.
