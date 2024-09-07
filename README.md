# Scrapyng
##### by @jeanleles

##### Uma aplicação para fazer o scrap de páginas web, pegando os seus títulos (h1 e h2) e parágrafos (p). Caso você deseje ler os textos de uma página, mas não está sendo possível devido a algum modal, popup ou tarja que esteja na frente do conteúdo da página, tipo exigência de login, aceite de termos e cookies ou assinatura, você pode utilizar esta aplicação para obter o conteúdo da página apenas colocando a sua URL.

## 1. Tecnologias Utilizadas

- **Python**: Para o backend, usando Flask para criar a API que faz o scraping.
- **Flask**: Framework web para o backend em Python.
- **Beautiful Soup**: Biblioteca Python para extração de dados de arquivos HTML e XML.
- **Requests**: Biblioteca Python para fazer requisições HTTP.
- **JavaScript**: Para o frontend, manipulando as requisições e exibindo os resultados.
- **http-server**: Servidor simples para hospedar o frontend.
- **PM2**: Gerenciador de processos para manter a aplicação online continuamente.

## Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/scrapyng.git
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
#### Instalar o http-server
##### No diretório frontend, instale o http-server globalmente para servir os arquivos HTML, CSS e JavaScript:

```bash
npm install -g http-server
```

### 4. Manter a Aplicação Online com PM2
#### Para manter a aplicação rodando continuamente, usaremos o PM2.
#### Instalar o PM2
```bash
npm install -g pm2
```

#### Iniciar o Backend com PM2
##### Navegue até o diretório do backend e inicie o backend usando PM2:
```bash
pm2 start start-backend.sh --name backendScraping
```

#### Iniciar o Frontend com PM2
##### Navegue até o diretório do frontend e inicie o frontend usando PM2:
```bash
pm2 start start-frontend.sh --name frontendServer
```

#### Verificar os Processos
##### Para listar os processos em execução com o PM2, utilize:
```bash
pm2 list
```

#### Verificar os Processos
##### Para listar os processos em execução com o PM2, utilize:
```bash
pm2 save
pm2 startup
```

### 5. Utilização da Aplicação
#### 1. Acesse o frontend através do navegador usando o endereço fornecido pelo http-server, por exemplo, http://localhost:8080.
#### 2. Insira a URL da página que deseja fazer o scraping no campo de entrada.
#### 3. Clique no botão para obter os resultados.
#### 4. O conteúdo da página (tags h1, h2 e p) será exibido logo abaixo.

### Estrutura do Projeto

SCRAPYNG/
│
├── backend/                  
│   ├── __pycache__/          
│   ├── app.py                # Arquivo principal do Flask
│   ├── scrapying.py          # Arquivo com as funções de scraping
│   └── start-backend.sh      # Script para iniciar o backend
│
├── frontend/                 
│   ├── index.html            # Página principal do frontend
│   ├── script.js             # Script JavaScript para a interação
│   ├── styles.css            # Estilos CSS para o frontend
│   └── start-frontend.sh     # Script para iniciar o frontend
│
└── README.md                 # Documentação do projeto
