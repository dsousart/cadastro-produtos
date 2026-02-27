# Web (Wave 2)

Scaffold inicial do frontend (Next.js 14) para consumir a API implementada na Wave 1.

## Objetivo deste scaffold

- validar bootstrap de frontend (`web/`)
- testar conectividade com `GET /healthz`
- preparar base para formulario, listagem e painel de `generation-jobs`

## Setup local

1. Instale dependencias:
   - `cd web`
   - `npm install`
2. Crie `.env.local` a partir de `web/.env.example`
3. Suba a API (`uvicorn api.main:app --reload`)
4. Rode:
   - `npm run dev`

## Variaveis

- `NEXT_PUBLIC_API_BASE_URL` (default `http://localhost:8000`)

## Testes (Playwright)

### Pre-requisitos

- Dependencias instaladas em `web/` (`npm install`)
- Browser do Playwright instalado:
  - `npx playwright install chromium`

### Execucao local

1. `npm run lint`
2. `npm run typecheck`
3. `npm test`

Observacoes:

- `npm test` usa `web/playwright.config.ts` e sobe o Next em `127.0.0.1:3100`.
- A suite smoke inicial cobre `/produtos`, `/gerar` e `/jobs`.

### Comandos uteis

- UI runner: `npm run test:ui`
- Rodar um arquivo: `npx playwright test tests/e2e/smoke.spec.ts`
