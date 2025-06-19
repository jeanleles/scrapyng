async function fetchScrapingResults() {
  const url = document.getElementById('urlInput').value;
  const resultContainer = document.getElementById('resultContent');
  const summaryContainer = document.getElementById('summaryContainer');
  const scrapeSection = document.getElementById('scrapeSection');
  const spinner = document.getElementById('loadingSpinner');

  // Limpa mensagens anteriores
  resultContainer.innerHTML = '';
  summaryContainer.innerHTML = '';
  scrapeSection.style.display = 'none';

  // Validação: se não houver URL, exibe erro unificado e retorna
  if (!url || url.trim() === '') {
    summaryContainer.innerHTML = '<div><strong>Erro:</strong> Informe uma URL válida para realizar o scraping.</div>';
    scrapeSection.style.display = 'block';
    return;
  }

  spinner.style.display = 'flex';

  try {
    // Chama o backend para obter o resumo
    const summaryResponse = await fetch('http://172.21.2.152:5555/summarize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url })
    });
    if (summaryResponse.ok) {
      const summaryData = await summaryResponse.json();
      if (summaryData.summary) {
        summaryContainer.innerHTML = `<div><strong>Resumo:</strong> ${summaryData.summary}</div>`;
      } else {
        summaryContainer.innerHTML = '<div><strong>Resumo:</strong> Não foi possível gerar um resumo.</div>';
      }
    } else {
      summaryContainer.innerHTML = '<div><strong>Resumo:</strong> Erro ao gerar resumo.</div>';
    }

    // Chama o backend para obter o scraping detalhado
    const response = await fetch('http://172.21.2.152:5555/scrape', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url })
    });

    if (!response.ok) {
      const errorData = await response.json();
      resultContainer.textContent = `Erro: ${errorData.error}`;
      spinner.style.display = 'none';
      scrapeSection.style.display = 'block';
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

    spinner.style.display = 'none';
    scrapeSection.style.display = 'block';

  } catch (error) {
    summaryContainer.innerHTML = `<div><strong>Erro:</strong> ${error.message}</div>`;
    resultContainer.innerHTML = '';
    spinner.style.display = 'none';
    scrapeSection.style.display = 'block';
  }
}

async function fetchOnlySummary() {
  const url = document.getElementById('urlInput').value;
  const summaryContainer = document.getElementById('summaryContainer');
  const resultContainer = document.getElementById('resultContent');
  const scrapeSection = document.getElementById('scrapeSection');
  const spinner = document.getElementById('loadingSpinner');

  summaryContainer.innerHTML = '';
  resultContainer.innerHTML = '';
  scrapeSection.style.display = 'none';

  // Validação: se não houver URL, exibe erro unificado e retorna
  if (!url || url.trim() === '') {
    summaryContainer.innerHTML = '<div><strong>Erro:</strong> Informe uma URL válida para gerar o resumo.</div>';
    scrapeSection.style.display = 'block';
    return;
  }

  spinner.style.display = 'flex';

  try {
    const summaryResponse = await fetch('http://172.21.2.152:5555/summarize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url })
    });
    if (summaryResponse.ok) {
      const summaryData = await summaryResponse.json();
      if (summaryData.summary) {
        summaryContainer.innerHTML = `<div><strong>Resumo:</strong> ${summaryData.summary}</div>`;
      } else {
        summaryContainer.innerHTML = '<div><strong>Resumo:</strong> Não foi possível gerar um resumo.</div>';
      }
    } else {
      summaryContainer.innerHTML = '<div><strong>Resumo:</strong> Erro ao gerar resumo.</div>';
    }
    spinner.style.display = 'none';
    scrapeSection.style.display = 'block';
  } catch (error) {
    summaryContainer.innerHTML = `<div><strong>Erro:</strong> ${error.message}</div>`;
    resultContainer.innerHTML = '';
    spinner.style.display = 'none';
    scrapeSection.style.display = 'block';
  }
}

// Atualiza a visibilidade do botão X conforme o texto do input
const urlInput = document.getElementById('urlInput');
const urlBox = document.querySelector('.url-box');
if (urlInput && urlBox) {
  urlInput.addEventListener('input', function() {
    if (urlInput.value.trim() !== '') {
      urlBox.classList.add('has-text');
    } else {
      urlBox.classList.remove('has-text');
    }
  });
}

function clearUrlInput() {
  const input = document.getElementById('urlInput');
  input.value = '';
  const urlBox = document.querySelector('.url-box');
  if (urlBox) urlBox.classList.remove('has-text');
  input.focus();
}

// Foco automático no input ao carregar a página
window.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('urlInput');
  if (input) input.focus();
});
