import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Scrapying | Web Scraper',
  description: 'Extraia e sintetize conteúdo da web com rapidez.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
