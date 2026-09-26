## corrigir o SSRF

- Este é o ponto mais importante.

Hoje temos:
`url = data.get('url')
response = requests.get(url, timeout=REQUEST_TIMEOUT)`

Ou seja, se a aplicação estiver acessível publicamente, alguém pode tentar algo como:
http://127.0.0.1:3000
http://localhost:5555
http://192.168.1.1
http://10.0.0.1
http://172.17.0.1
http://169.254.169.254

O último é especialmente importante em ambientes cloud porque o endereço 169.254.169.254 é usado por serviços de metadata de várias plataformas.

E não basta simplesmente bloquear 127.0.0.1: existe o problema de DNS rebinding.

Além disso, requests segue redirects por padrão. Então:

https://site-legitimo.com
↓ 302
http://127.0.0.1:xxxx

também precisa ser tratado.

Minha recomendação

Antes do deploy, alterar o backend para:

aceitar somente http:// e https://;
rejeitar IPs privados;
rejeitar loopback;
rejeitar link-local;
rejeitar multicast;
rejeitar redes reservadas;
rejeitar localhost;
validar cada redirect;
limitar tamanho da resposta;
limitar timeout;
limitar número de redirects;
limitar tamanho da URL;
limitar tamanho do conteúdo enviado ao Gemini;
tratar Content-Type;
não permitir esquemas como file://, ftp://, etc.;
adicionar rate limit.

Esse é um requisito de produção para este aplicativo, não um "extra".

## Corrigir também o CORS

Hoje:

CORS(app)

significa, na prática, permitir requisições cross-origin de forma ampla.

Como vamos colocar frontend e backend atrás do mesmo domínio, o ideal é nem depender de CORS.

Por exemplo:

https://scrapyng.jeanleles.com

será o único domínio público.

O navegador conversa com:

https://scrapyng.jeanleles.com/api/scrape

e o Next.js encaminha internamente para:

http://backend:5555

O README já descreve exatamente essa arquitetura.

Portanto, podemos remover o CORS global ou restringi-lo explicitamente ao domínio da aplicação.

## Rate limiting

Este aplicativo é particularmente adequado para rate limiting porque existem dois recursos potencialmente caros:

Scraping
POST /scrape

consome:

conexão externa;
CPU;
memória;
banda;
tempo de worker.
Gemini
POST /summarize

além disso pode gerar custo financeiro.

Eu colocaria inicialmente algo como:

/scrape
10 requisições/minuto/IP

/summarize
3 requisições/minuto/IP

Podemos ajustar depois com base no uso real.

E também colocaria limite de:

URL: ~2 KB
response HTML: alguns MB
texto enviado ao Gemini: limite definido

## Docker: endurecer os containers

O Dockerfile atual do backend é simples:

FROM python:3.12-slim
...
CMD ["gunicorn", "--bind", "0.0.0.0:5555", ...]

E o frontend usa node:22-alpine e Next.js standalone. Isso é bom porque o runtime final é pequeno.

Mas eu acrescentaria:

Backend
usuário não-root;
filesystem read-only;
no-new-privileges;
limite de memória;
limite de CPU;
pids_limit;
log rotation;
healthcheck;
cap_drop: ALL;
somente as capabilities estritamente necessárias — provavelmente nenhuma.

Exemplo conceitual no Compose:

security_opt:

- no-new-privileges:true

cap_drop:

- ALL

read_only: true

tmpfs:

- /tmp

mem_limit: 512m
cpus: "1.0"

pids_limit: 100

## Não expor o backend

Aqui o projeto já está fazendo a coisa certa.

Hoje:

backend:
expose: - "5555"

e não:

ports:

- "5555:5555"

Não vamos mudar isso.

O backend será acessível somente dentro da rede Docker.

## Frontend

Também manteremos:

ports:

- "127.0.0.1:3000:3000"

Isso significa:

Internet
X
│
└── :3000

Caddy
│
└── 127.0.0.1:3000

O único serviço diretamente exposto à Internet continuará sendo:

80 → Caddy
443 → Caddy

## Estrutura no VPS

Seguindo a organização que já usamos no seu VPS:

~/infra/
├── apps/
│ ├── password-generator/
│ └── scrapyng/
│
└── caddy/

Eu criaria:

mkdir -p ~/infra/apps/scrapyng
cd ~/infra/apps/scrapyng

E teremos algo como:

~/infra/apps/scrapyng/
├── compose.yml
├── .env
└── deploy.sh

Não vamos clonar o repositório inteiro no VPS.

O VPS receberá apenas:

Compose;
configuração;
secrets;
imagem Docker.

O código-fonte ficará no GitHub.

Isso reduz bastante a superfície de ataque e deixa o deploy mais limpo.

## GHCR

Vamos usar:

ghcr.io/jeanleles/scrapyng-backend
ghcr.io/jeanleles/scrapyng-frontend

Mas eu prefiro ainda mais:

ghcr.io/jeanleles/scrapyng-backend:<git-sha>
ghcr.io/jeanleles/scrapyng-frontend:<git-sha>

Por exemplo:

ghcr.io/jeanleles/scrapyng-backend:7c91a2e
ghcr.io/jeanleles/scrapyng-frontend:7c91a2e

Assim sabemos exatamente qual código está em produção.

Nada de produção depender de latest.

## Compose de produção

O Compose do repositório é atualmente orientado para build local.

No VPS eu criaria um Compose separado:

services:

backend:
image: ghcr.io/jeanleles/scrapyng-backend:${IMAGE_TAG}

    env_file:
      - .env

    expose:
      - "5555"

    environment:
      PORT: 5555
      WEB_CONCURRENCY: 2
      SCRAPE_REQUEST_TIMEOUT: 15
      FLASK_DEBUG: "false"

    restart: unless-stopped

    security_opt:
      - no-new-privileges:true

    cap_drop:
      - ALL

    read_only: true

    tmpfs:
      - /tmp

    mem_limit: 512m
    cpus: "1.0"
    pids_limit: 100

    healthcheck:
      test:
        [
          "CMD",
          "python",
          "-c",
          "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5555/health')"
        ]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

frontend:
image: ghcr.io/jeanleles/scrapyng-frontend:${IMAGE_TAG}

    environment:
      NODE_ENV: production
      PORT: 3000
      HOSTNAME: 0.0.0.0

    ports:
      - "127.0.0.1:3000:3000"

    depends_on:
      backend:
        condition: service_healthy

    restart: unless-stopped

    security_opt:
      - no-new-privileges:true

    cap_drop:
      - ALL

    mem_limit: 512m
    cpus: "1.0"

    healthcheck:
      test:
        [
          "CMD",
          "node",
          "-e",
          "fetch('http://127.0.0.1:3000').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"
        ]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

Depois ajustaremos isso conforme os Dockerfiles reais e os recursos disponíveis na sua OCI.

## Um ponto importante sobre Gemini

Hoje o código usa:

models/gemini-2.5-flash

e manda para o modelo todo o conteúdo extraído:

prompt = f"... {full_text}"

Isso precisa de limite.

Imagine alguém fornecendo uma página gigantesca:

10 MB
50 MB
100 MB

Você pode ter:

download grande
↓
memória
↓
parsing BeautifulSoup
↓
texto gigante
↓
Gemini
↓
custo

Portanto vamos colocar um limite explícito antes do Gemini.

## Resiliência do scraping

Eu também mudaria:

timeout=20

para um timeout configurável, por exemplo:

connect timeout: 5s
read timeout: 15s

em vez de simplesmente:

timeout=20

E limitaria redirects.

Também precisamos decidir se queremos permitir:

http://
https://

ou somente:

https://

Minha sugestão inicial é permitir os dois para compatibilidade, mas bloquear destinos inseguros.

## O que eu quero evitar

Não faremos:

❌ backend:5555 exposto na Internet
❌ frontend:3000 exposto na Internet
❌ GEMINI_API_KEY no Git
❌ GEMINI_API_KEY no Dockerfile
❌ deploy usando root
❌ build diretamente no VPS
❌ produção usando latest
❌ git pull em produção
❌ PM2
❌ Nginx + Caddy simultaneamente
❌ banco sem necessidade
❌ volumes desnecessários
❌ CORS \*
❌ scraping sem proteção SSRF
❌ ausência de rate limit
❌ deploy sem healthcheck
❌ deploy sem rollback

## O que já temos a favor

O projeto já traz uma base relativamente boa:

Item Situação
Flask + Gunicorn ✅
Next.js standalone ✅
Docker ✅
Docker Compose ✅
Backend sem porta pública ✅
Frontend localhost ✅
Healthcheck backend ✅
Healthcheck frontend ✅
Caddy ✅ arquitetura existente
/health ✅
.env separado ✅
Gemini por variável de ambiente ✅
CI/CD anterior no seu VPS ✅ padrão já estabelecido
SSRF protection ❌ precisa implementar
Rate limiting ❌
limites de payload ❌
containers non-root ⚠️ verificar/implementar
rollback automatizado ❌
imagens imutáveis ❌
security scanning ❌

O próprio README confirma que a aplicação já foi pensada para Docker Compose + Caddy e que o backend não deve ser publicado diretamente.

## Minha recomendação para nosso próximo passo

Não começaria ainda pelo VPS.

Primeiro eu faria uma pequena preparação no repositório:

1. corrigir SSRF
2. corrigir CORS
3. adicionar rate limiting
4. adicionar limites de scraping
5. endurecer Dockerfiles
6. criar testes
7. criar compose de produção
8. criar GitHub Actions
9. só então publicar na OCI

Isso evita colocar uma aplicação deliberadamente construída para acessar URLs externas na Internet antes de resolver a principal classe de vulnerabilidade dela.

Preciso de 3 informações suas
Qual domínio/subdomínio você quer usar?
Ex.: scrapyng.jeanleles.com

Confirma que vamos usar a mesma arquitetura do seu VPS atual?

~/infra/apps/<app>
Caddy
Docker
rede externa webnetwork
GHCR
GitHub Actions → SSH → OCI
Você quer que eu conduza também as alterações no código do Scrapyng antes do deploy?
Eu recomendo sim, principalmente por causa do SSRF.

Se você confirmar essas três coisas, no próximo passo eu posso montar o procedimento operacional completo, comando por comando, começando pelo endurecimento do repositório e entregando os arquivos que precisaremos criar/modificar (Dockerfile, compose.prod.yml, deploy.sh, workflow .github/workflows/deploy.yml e Caddyfile), e depois seguimos juntos para executar no Ubuntu da OCI.
