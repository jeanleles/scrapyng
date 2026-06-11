#!/bin/bash
# Ativa o ambiente virtual
source venv/bin/activate

# Define as variáveis de ambiente para o Flask
export FLASK_APP=app.py
export FLASK_ENV=development

# Inicia o servidor Flask, escutando em todas as interfaces de rede
echo "Iniciando o servidor Flask em http://0.0.0.0:5555"
flask run --host=0.0.0.0 --port=5555