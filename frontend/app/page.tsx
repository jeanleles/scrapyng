'use client';

import { useMemo, useState } from 'react';
import {
  Activity,
  ArrowUp,
  Check,
  CheckCircle2,
  Clipboard,
  ClipboardPaste,
  Code2,
  Copy,
  FileText,
  Gauge,
  Link as LinkIcon,
  LoaderCircle,
  Menu,
  Sparkles,
  Terminal,
  UserRound,
  X,
  Zap,
} from 'lucide-react';

type ScrapeResult = Record<string, string[]>;
type ResultMode = 'scrape' | 'summary';
type ApiState = 'idle' | 'loading' | 'success' | 'error';

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? '/api';
const sections = [
  ['h1', 'Títulos principais'],
  ['h2', 'Subtítulos'],
  ['h3', 'Seções'],
  ['p', 'Parágrafos'],
  ['blockquote', 'Citações'],
  ['ul_li', 'Listas'],
] as const;

export default function Home() {
  const [url, setUrl] = useState('');
  const [summary, setSummary] = useState('');
  const [scrape, setScrape] = useState<ScrapeResult | null>(null);
  const [state, setState] = useState<ApiState>('idle');
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);
  const [mode, setMode] = useState<ResultMode>('scrape');
  const [cleanHtml, setCleanHtml] = useState(true);

  const extractedText = useMemo(() => {
    if (!scrape) return '';
    return sections.flatMap(([key]) => scrape[key] ?? []).join('\n\n');
  }, [scrape]);

  async function request(path: string) {
    const response = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url.trim() }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error ?? 'Não foi possível concluir a operação.');
    return data;
  }

  async function run(action: ResultMode) {
    if (!url.trim()) {
      setError('Informe uma URL válida para continuar.');
      setState('error');
      return;
    }
    setMode(action);
    setState('loading');
    setError('');
    if (action === 'scrape') setScrape(null);
    else setSummary('');

    try {
      if (action === 'scrape') {
        const [scrapeData, summaryData] = await Promise.all([request('/scrape'), request('/summarize')]);
        setScrape(scrapeData);
        setSummary(summaryData.summary ?? 'Não foi possível gerar um resumo.');
      } else {
        const data = await request('/summarize');
        setSummary(data.summary ?? 'Não foi possível gerar um resumo.');
      }
      setState('success');
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Erro inesperado.');
      setState('error');
    }
  }

  async function pasteUrl() {
    try {
      const text = await navigator.clipboard.readText();
      if (text) setUrl(text);
    } catch {
      setError('Não foi possível acessar a área de transferência.');
      setState('error');
    }
  }

  async function copySummary() {
    if (!summary) return;
    await navigator.clipboard.writeText(summary);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  }

  return (
    <main className="min-h-screen bg-[var(--surface)]">
      <header className="fixed top-0 z-50 w-full border-b border-[var(--outline-variant)]/30 bg-[var(--surface)]/85 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-[1360px] items-center justify-between gap-3 px-4 sm:px-6">
          <div className="flex min-w-0 items-center gap-3">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[var(--primary-container)] text-white"><Code2 size={17} /></div>
            <div className="min-w-0">
              <div className="flex items-center gap-2"><span className="truncate font-['Plus_Jakarta_Sans'] text-lg font-semibold">Scrapying</span><span className="font-mono text-[11px] text-[var(--muted)]">/ Scraper</span></div>
              <div className="flex items-center gap-1.5 font-mono text-[10px] font-semibold tracking-wider text-[var(--tertiary)]"><span className="h-2 w-2 rounded-full bg-[var(--tertiary)] shadow-[0_0_10px_var(--tertiary)]" /> ENGINE V2.4 ACTIVE</div>
            </div>
          </div>
          <div className="flex items-center gap-3"><button aria-label="Configurações" className="rounded-lg p-2 text-[var(--muted)] hover:bg-[var(--surface-high)] hover:text-white"><Menu size={20} /></button><div className="flex h-8 w-8 items-center justify-center rounded-full bg-[var(--primary)] text-[#002682]"><UserRound size={17} /></div></div>
        </div>
      </header>

      <div className="mx-auto flex w-full max-w-[1360px] flex-col px-4 pb-8 pt-24 sm:px-6 lg:px-8">
        <section className="mx-auto flex w-full max-w-[880px] flex-col items-center text-center">
          <div className="mb-3 inline-flex items-center gap-1.5 rounded-full bg-[var(--surface-high)] px-3 py-1 font-mono text-[11px] font-semibold tracking-wider text-[var(--tertiary)]"><Zap size={14} /> EXTRAÇÃO INSTANTÂNEA</div>
          <h1 className="font-['Plus_Jakarta_Sans'] text-3xl font-bold tracking-tight text-[var(--on-surface)] sm:text-[40px] sm:leading-[48px]">Web Scraping &amp; <span className="text-[var(--primary)]">Resumo IA</span></h1>
          <p className="mt-2 max-w-lg text-sm leading-6 text-[var(--muted)]">Extraia artigos, dados limpos e sintetize conteúdo automaticamente em segundos.</p>
        </section>

        <section className="mx-auto mt-8 w-full max-w-[880px] rounded-xl bg-[var(--surface-container)] p-2 shadow-2xl">
          <div className="flex items-center gap-2 rounded-lg bg-[var(--surface-low)] px-3 py-2.5 focus-within:ring-1 focus-within:ring-[var(--primary-container)]">
            <LinkIcon className="shrink-0 text-[var(--outline)]" size={19} /><input aria-label="URL para scraping" className="min-w-0 flex-1 bg-transparent font-mono text-sm text-[var(--on-surface)] outline-none placeholder:text-[var(--outline)]" onChange={(event) => setUrl(event.target.value)} onKeyDown={(event) => event.key === 'Enter' && run('scrape')} placeholder="https://exemplo.com/artigo" type="url" value={url} /><button aria-label="Limpar URL" className="rounded p-1 text-[var(--muted)] hover:text-white" onClick={() => setUrl('')}><X size={17} /></button><button className="hidden items-center gap-1 rounded bg-[var(--surface-high)] px-2.5 py-1.5 font-mono text-[11px] font-semibold text-[var(--muted)] hover:text-white sm:flex" onClick={pasteUrl}><ClipboardPaste size={14} /> Colar</button>
          </div>
          <div className="grid grid-cols-1 gap-1.5 pt-1.5 sm:grid-cols-2"><button className="flex items-center justify-center gap-2 rounded-lg bg-[var(--primary-container)] px-3 py-3 font-['Plus_Jakarta_Sans'] text-sm font-semibold text-white hover:bg-blue-600" disabled={state === 'loading'} onClick={() => run('scrape')}>{state === 'loading' && mode === 'scrape' ? <LoaderCircle className="animate-spin" size={18} /> : <Code2 size={18} />} Fazer Scraping</button><button className="flex items-center justify-center gap-2 rounded-lg bg-[var(--surface-high)] px-3 py-3 font-['Plus_Jakarta_Sans'] text-sm font-semibold text-[var(--secondary)] hover:bg-[var(--surface-highest)]" disabled={state === 'loading'} onClick={() => run('summary')}>{state === 'loading' && mode === 'summary' ? <LoaderCircle className="animate-spin" size={18} /> : <Sparkles className="text-[var(--tertiary)]" size={18} />} Gerar Resumo</button></div>
        </section>

        <div className="mx-auto mt-2 flex w-full max-w-[880px] items-center gap-2 overflow-x-auto py-2 font-mono text-[11px] font-semibold whitespace-nowrap"><span className="text-[var(--muted)]">MODO:</span><button className={`rounded-full px-3 py-1 ${cleanHtml ? 'bg-[var(--primary)] text-[#002682]' : 'bg-[var(--surface-high)] text-[var(--muted)]'}`} onClick={() => setCleanHtml(!cleanHtml)}><CheckCircle2 className="mr-1 inline" size={13} /> Limpar HTML</button><button className="rounded-full bg-[var(--surface-high)] px-3 py-1 text-[var(--muted)]"><FileText className="mr-1 inline" size={13} /> Metadados</button><button className="rounded-full bg-[var(--surface-high)] px-3 py-1 text-[var(--muted)]"><Code2 className="mr-1 inline" size={13} /> Markdown</button></div>

        <div className="mx-auto mt-3 flex w-full max-w-[880px] items-center justify-between rounded-xl bg-[var(--surface-low)] p-2.5"><div className="flex items-center gap-3"><div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[var(--surface-highest)] text-[var(--tertiary)]"><Gauge size={20} /></div><div className="text-left"><div className="font-mono text-[11px] font-semibold tracking-wider text-[var(--tertiary)]">LATÊNCIA MÉDIA ~0.42s</div><div className="text-xs text-[var(--muted)]">Parser Python Headless Ativo</div></div></div><span className="rounded bg-[var(--surface-high)] px-2 py-1 font-mono text-[11px] font-semibold text-[var(--secondary)]">Gemini 2.5 Flash</span></div>

        {state === 'error' && <div className="mx-auto mt-4 w-full max-w-[880px] rounded-lg border border-red-400/30 bg-red-950/30 p-4 text-sm text-[var(--error)]">{error}</div>}
        {(state === 'success' || summary || scrape) && <Results summary={summary} scrape={scrape} extractedText={extractedText} copied={copied} onCopy={copySummary} />}

        <footer className="mt-12 flex flex-col items-center gap-1 text-center"><div className="flex items-center gap-1.5 font-mono text-[11px] font-semibold tracking-wider text-[var(--muted)]"><Terminal className="text-[var(--tertiary)]" size={15} /> POWERED BY PYTHON &amp; LLM CORE</div><span className="text-xs text-[var(--outline)]">por <a className="text-[var(--primary)] hover:underline" href="https://github.com/jeanleles">@jeanleles</a></span></footer>
      </div>
      <button aria-label="Voltar ao topo" className="fixed bottom-5 right-5 flex h-11 w-11 items-center justify-center rounded-full border border-[var(--outline-variant)] bg-[var(--surface-high)] text-[var(--muted)] shadow-xl hover:text-white" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}><ArrowUp size={19} /></button>
    </main>
  );
}

function Results({ summary, scrape, extractedText, copied, onCopy }: { summary: string; scrape: ScrapeResult | null; extractedText: string; copied: boolean; onCopy: () => void }) {
  return <section className="mx-auto mt-8 w-full max-w-[880px]"><div className="mb-3 flex items-center justify-between gap-3"><h2 className="flex items-center gap-1.5 font-['Plus_Jakarta_Sans'] text-lg font-semibold"><Sparkles className="text-[var(--tertiary)]" size={18} /> Resultado &amp; Resumo IA</h2><span className="hidden items-center gap-1 rounded bg-[var(--tertiary)]/15 px-2 py-1 font-mono text-[11px] font-semibold text-[var(--tertiary)] sm:flex"><CheckCircle2 size={13} /> Concluído</span></div><article className="rounded-xl border border-[var(--primary-container)]/50 bg-[var(--surface-container)] p-4 shadow-xl sm:p-5"><div className="flex items-center justify-between border-b border-[var(--outline-variant)] pb-3"><span className="flex items-center gap-1.5 font-mono text-[11px] font-semibold tracking-wider"><Sparkles className="text-[var(--tertiary)]" size={16} /> RESUMO EXECUTIVO (IA)</span><button className="flex items-center gap-1 rounded bg-[var(--surface-high)] px-2.5 py-1.5 font-mono text-[11px] font-semibold text-[var(--secondary)]" onClick={onCopy}>{copied ? <Check size={14} /> : <Copy size={14} />} {copied ? 'Copiado' : 'Copiar Resumo'}</button></div><p className="pt-4 text-sm leading-7 text-[var(--on-surface)]">{summary || 'O resumo será exibido aqui após a execução.'}</p><div className="mt-4 flex items-center justify-between border-t border-[var(--outline-variant)] pt-3 font-mono text-[10px] font-semibold text-[var(--muted)]"><span>Modelo: Gemini 2.5 Flash</span><span className="text-[var(--tertiary)]">Síntese concluída</span></div></article>{scrape && <article className="mt-4 rounded-xl bg-[var(--surface-low)] p-4 sm:p-5"><div className="flex items-center justify-between border-b border-[var(--outline-variant)] pb-3"><span className="flex items-center gap-1.5 font-mono text-[11px] font-semibold tracking-wider text-[var(--primary)]"><FileText size={16} /> CONTEÚDO EXTRAÍDO LIMPO</span><span className="flex items-center gap-1 font-mono text-[10px] font-semibold text-[var(--muted)]"><CheckCircle2 className="text-[var(--tertiary)]" size={14} /> HTML Sanitizado</span></div><div className="mt-4 flex items-center justify-between gap-3"><h3 className="font-['Plus_Jakarta_Sans'] text-lg font-semibold">Conteúdo da página</h3><button aria-label="Copiar conteúdo" className="rounded p-1.5 text-[var(--muted)] hover:bg-[var(--surface-high)] hover:text-white" onClick={() => navigator.clipboard.writeText(extractedText)}><Clipboard size={16} /></button></div><div className="mt-4 space-y-4 text-sm leading-7 text-[var(--on-surface)]">{sections.map(([key, label]) => (scrape[key]?.length ? <div key={key}><h4 className="mb-1 font-mono text-[11px] font-semibold uppercase tracking-wider text-[var(--secondary)]">{label}</h4>{scrape[key].map((text, index) => <p key={`${key}-${index}`} className="text-[var(--muted)]">{text}</p>)}</div> : null))}</div></article>}</section>;
}
