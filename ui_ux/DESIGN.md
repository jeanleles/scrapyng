---
name: Synthetic Intelligence Scraper
colors:
  surface: '#0c1322'
  surface-dim: '#0c1322'
  surface-bright: '#323949'
  surface-container-lowest: '#070e1d'
  surface-container-low: '#141b2b'
  surface-container: '#191f2f'
  surface-container-high: '#232a3a'
  surface-container-highest: '#2e3545'
  on-surface: '#dce2f7'
  on-surface-variant: '#c4c5d7'
  inverse-surface: '#dce2f7'
  inverse-on-surface: '#293040'
  outline: '#8e90a0'
  outline-variant: '#434655'
  surface-tint: '#b7c4ff'
  primary: '#b7c4ff'
  on-primary: '#002682'
  primary-container: '#1d4ed8'
  on-primary-container: '#cad3ff'
  inverse-primary: '#2151da'
  secondary: '#9ccaff'
  on-secondary: '#003257'
  secondary-container: '#03497a'
  on-secondary-container: '#87b9f0'
  tertiary: '#4edea3'
  on-tertiary: '#003824'
  tertiary-container: '#006a48'
  on-tertiary-container: '#60eeb1'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#dce1ff'
  primary-fixed-dim: '#b7c4ff'
  on-primary-fixed: '#001551'
  on-primary-fixed-variant: '#0039b5'
  secondary-fixed: '#d0e4ff'
  secondary-fixed-dim: '#9ccaff'
  on-secondary-fixed: '#001d35'
  on-secondary-fixed-variant: '#03497a'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#0c1322'
  on-background: '#dce2f7'
  surface-variant: '#2e3545'
typography:
  display-hero:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  display-hero-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: 0em
  body-base:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.01em
  code-base:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: -0.01em
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.06em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system is engineered for developers, researchers, and knowledge workers who rely on rapid web extraction and automated LLM synthesis. Moving away from utilitarian, unpolished scripts, the interface embodies a sophisticated **Developer Minimalist & Neon-Dark** aesthetic—blending the discipline of high-performance developer command centers with the polish of modern SaaS productivity tools.

The interface prioritizes dense, distraction-free consumption. The visual language conveys speed, deterministic accuracy, and cryptographic clarity. Users should feel empowered and focused, experiencing zero cognitive friction when transitioning from raw URL ingestion to structured markdown consumption and metadata auditing.

## Colors

The palette is anchored in an uncompromising deep dark foundation, replacing harsh pure blacks with rich midnight tones and subtle cold-tinted boundaries.

- **Surface Layers:**
  - `Canvas / Background`: `#0A0A0A` — Void black canvas establishing deep contrast.
  - `Card / Surface Default`: `#111827` — Deep obsidian slate for content modules and readouts.
  - `Surface Elevated / Hover`: `#1F2937` — Elevated card and interactive hover fills.
  - `Border Subtle`: `#1F2937` — Subtle delineation between structural containers.
  - `Border Interactive`: `#374151` — Distinct hairline borders for inputs, buttons, and segmented controls.

- **Accents & Semantics:**
  - `Primary Action`: `#1D4ED8` — Vibrant tech cobalt used for active extractions, primary triggers, and core focus rings.
  - `Primary Highlight`: `#93C5FD` — High-legibility icy blue for active tab text, syntax tokens, and AI summaries.
  - `Success / Scraping Active`: `#10B981` — Terminal emerald for live scraping indicators, successful 200 HTTP payloads, and copy confirmations.
  - `Text High-Contrast`: `#FFFFFF` — Pure white for titles, values, and primary actions.
  - `Text Secondary`: `#94A3B8` — Cool slate for body copy, markdown paragraphs, and parameter keys.
  - `Text Muted`: `#64748B` — De-emphasized timestamps, inactive shortcuts, and protocol markers.

## Typography

The type system pairs modern, geometric clarity with developer-grade monospaced precision. 

- **Display & Headlines (`Plus Jakarta Sans`)**: Delivers geometric crispness without aggressive quirks. Tight negative letter spacing reinforces technical cohesion.
- **Body & Longform Reading (`Inter`)**: Tuned for maximum readability within extracted markdown payloads and dense summary paragraphs. Generous line heights (`1.6x`) prevent reading fatigue.
- **Data, Status & Code (`JetBrains Mono`)**: Handles all API response metrics, URL strings, HTTP status pills, markdown code fences, and keyboard shortcuts. All numeric counters use tabular figures (`font-variant-numeric: tabular-nums`).

## Layout & Spacing

The layout is built around a single focused command column for high-speed utility, transitioning to a flexible split layout when evaluating side-by-side data on ultra-wide screens.

- **Main Workstation Canvas**: Centered max-width container at `880px` for optimal document reading length and distraction-free URL processing. On monitors `>1440px`, an optional inspection drawer docks to the right side (width `380px`).
- **Vertical Rhythm**:
  - `Canvas Margins`: `2rem` (`32px`) on desktop, collapsing to `1rem` (`16px`) on mobile viewports.
  - Component gaps adhere to a 4px baseline grid, stepping consistently through `8px` (`space-sm`), `16px` (`space-md`), and `24px` (`space-lg`).
- **Responsive Architecture**:
  - **Desktop (1024px+)**: Unified URL bar with integrated button trigger cluster. Inline segment tabs toggling raw markdown, executive summary, and DOM tree.
  - **Mobile (<768px)**: Input remains fixed at the top with auto-focus preservation; auxiliary triggers (Scrape, Summarize, Copy) convert into a floating bottom docked toolbar (`h-14`) with haptic-ready touch targets.

## Elevation & Depth

Visual depth is achieved through delicate surface luminescence and razor-sharp borders rather than heavy, diffuse drop shadows.

- **Level 0 (Canvas Base)**: `#0A0A0A` flat void.
- **Level 1 (Card Container)**: Layered `#111827` surface framed by a single-pixel hairline border (`1px solid #1F2937`). No box shadow; purely tonal definition.
- **Level 2 (Floating Action Bars / Modals)**: `#111827` with a subtle backdrop filter (`backdrop-blur-md` at 85% opacity), bound by `1px solid #374151` and an ambient shadow (`box-shadow: 0 12px 32px -4px rgba(0, 0, 0, 0.65), 0 4px 12px -2px rgba(0, 0, 0, 0.4)`).
- **Interactive Focus Glows**: When active, primary inputs and CTA buttons project a subtle outer electromagnetic aura (`0 0 0 1px #1D4ED8, 0 0 20px -4px rgba(29, 78, 216, 0.45)`).

## Shapes

The design uses a clean, disciplined `0.5rem` (`8px`) baseline border radius, conveying precision tooling rather than playful consumer software.

- **Inputs, Buttons, and Cards**: Strictly `rounded-md` (`8px`) to maintain structural rhythm across nested elements.
- **Status Pills, HTTP Badges, and Micro Counters**: Use `rounded-full` (`9999px`) to immediately separate runtime indicators and tags from executable rectangular controls.
- **Outer Application Containers**: `rounded-lg` (`12px` to `16px`) on desktop viewports to soften large monolithic screen wrappers.

## Components

### 1. Unified Command Input
- **Architecture**: A cohesive, high-density search capsule combining the URL protocol icon, clear button, and integrated dual triggers.
- **Styling**: Background `#111827`, border `1px solid #374151`. Height is fixed at `52px` with internal right-side button cluster padding of `4px`.
- **States**: Focus state triggers border `#1D4ED8` alongside the ambient blue aura glow. Invalid URLs highlight the border in `#EF4444`.

### 2. Action Buttons & Triggers
- **Primary Action (Scrape / Run)**: Background `#1D4ED8`, text `#FFFFFF`, font `Plus Jakarta Sans` semi-bold (`14px`). Hover elevates to `#2563EB`. Active state scales subtly (`scale-98`).
- **Secondary Action (AI Summarize)**: Background `transparent`, border `1px solid #374151`, text `#93C5FD`. On hover, background shifts to `rgba(29, 78, 216, 0.12)` with border `#1D4ED8`.
- **Utility Buttons (Copy, Download, Raw View)**: Compact icon-only or icon-text elements styled in subtle slate tones with micro-tooltip confirmations.

### 3. View Switcher (Segmented Tabs)
- **Container**: Inset track styled with `#0A0A0A` background, `1px solid #1F2937`, padding `4px`, `rounded-md`.
- **Tab Elements**: "AI Summary", "Raw Content (Markdown)", and "Parsed Metadata".
- **Active Tab**: Surface `#1F2937` with crisp `#FFFFFF` text and a discrete bottom indicator or subtle edge glow; inactive tabs sit at `#94A3B8` on transparent.

### 4. Status Badges & Pills
- **Scraping Status Indicator**: Pill with pulsing green dot (`#10B981`) and uppercase label `JetBrains Mono` 11px (e.g., `200 OK`, `RUNNING...`, `PARSED 4.2KB`).
- **AI Model Badge**: Cyan-tinted badge (`rgba(147, 197, 253, 0.1)`) with text `#93C5FD` indicating extraction parameters (e.g., `GPT-4o Mini Summary`).

### 5. Content Presentation Card (Reader Module)
- **Container**: Layered `#111827` shell with a sticky module header housing document statistics (word count, reading time, extracted timestamp) and quick-action icon buttons.
- **Markdown Typography Styling**:
  - Headings: Crisp `#FFFFFF` with automatic anchor link generators on hover.
  - Body paragraphs: `#94A3B8` with highlighted key sentences rendered in `#E2E8F0`.
  - Code blocks: Framed in `#0A0A0A` sub-panels with border `1px solid #1F2937`, copy-all trigger, and syntax highlighting matching the palette.

### 6. Mobile Floating Action Bar
- Docked to bottom viewport with `safe-area-inset-bottom`.
- Full-width frosted container housing primary execution and mode toggle switches within thumb's reach, keeping the main card space 100% focused on reading.