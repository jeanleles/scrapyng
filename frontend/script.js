async function fetchScrapingResults() {
  const url = document.getElementById('urlInput').value;
  const resultContainer = document.getElementById('resultContent');
  resultContainer.innerHTML = '<p>Carregando...</p>';

  try {
    const response = await fetch('http://172.20.70.254:5555/scrape', { // 172.20.70.254 - IP da minha VM Ubuntu no WSL, pode ser localhost ou 172.0.0.1
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url })
    });

    if (!response.ok) {
      const errorData = await response.json();
      resultContainer.textContent = `Erro: ${errorData.error}`;
      return;
    }

    const data = await response.json();

    // Limpar o conteúdo anterior
    resultContainer.innerHTML = '';

    // Adicionar os textos de <h1>, <h2> e <p> ao HTML dinamicamente
    data.h1.forEach(text => {
      const h1Element = document.createElement('h1');
      h1Element.textContent = text;
      resultContainer.appendChild(h1Element);
    });

    data.h2.forEach(text => {
      const h2Element = document.createElement('h2');
      h2Element.textContent = text;
      resultContainer.appendChild(h2Element);
    });

    data.p.forEach(text => {
      const pElement = document.createElement('p');
      pElement.textContent = text;
      resultContainer.appendChild(pElement);
    });

  } catch (error) {
    resultContainer.textContent = `Erro: ${error.message}`;
  }
}
