# Wave 2 - Frontend Kickoff (Estado Parcial)

**Data:** 2026-02-26  
**Status:** Base funcional da Wave 2 implementada (frontend + proxies + fluxos principais)

## Entregas desta etapa

- `web/` criado com base Next.js 14 + TypeScript
- pagina inicial com health check da API (`/healthz`)
- formulario inicial para `POST /api/v1/products` (via proxy Next em `/api/products`)
- listagem paginada inicial de produtos (via proxy Next em `/api/products`)
- busca textual backend-driven (`q`) com debounce na listagem
- ordenacao (`sort_by`, `sort_dir`) integrada na listagem
- detalhe de produto por selecao na tabela (`GET /api/v1/products/{id}`)
- resumo visual no detalhe (ID, SKU, status, score)
- badges visuais de status/score na tabela
- painel inicial de `generation-jobs` com criacao + polling (via proxies Next)
- refresh automatico da listagem e foco no item novo (create product / job concluido)
- presets de filtros na listagem (`generated`, `score >= 80`, limpar)
- acoes de copiar (`product_id`, `sku`, `job_id`) com um clique
- JSONs colapsaveis (detalhe, `input_payload`, `output_payload`, status de job, resposta de create)
- indicador visual de polling ativo no painel de jobs
- helper de payload multi-item para `generation-jobs` (duplica item base com SKU incremental)
- visualizacao resumida de resultados do job (SKU, status, `product_id`, erro)
- persistencia de preferencias no painel de jobs (`polling automatico`, `status JSON colapsado`)
- persistencia de filtros/ordenacao da listagem de produtos (`busca`, `status`, `score`, `sort`, `limit`)
- navegacao por tabs no dashboard (`Gerar`, `Produtos`, `Jobs`, `Health`) com persistencia da tab ativa
- rotas reais por URL para operacao (`/gerar`, `/produtos`, `/jobs`, `/health`) com tabs mantendo navegacao
- deep-linking de filtros/ordenacao da listagem via query params em `/produtos` (`q`, `status`, `min_score`, `sort`, `limit`, `offset`, `focus`)
- acao de copiar link da visao atual em `/produtos` (compartilhamento rapido de filtros)
- presets de links operacionais em `/produtos` (`Revisao editorial`, `Aprovados`, `Score alto`)
- acao de resetar visao em `/produtos` (limpa query params e estado da listagem)
- empty states guiados em `Produtos` e `Jobs` com CTA operacional
- smoke E2E inicial com Playwright para `/produtos`, `/gerar` e `/jobs`
- CI de frontend (`.github/workflows/web-ci.yml`) com `lint`, `typecheck` e smoke E2E
- configuracao inicial de env (`web/.env.example`)
- `README` de bootstrap local

## Validacao local executada

- `npm install` em `web/`
- `npm run dev` (Next.js) com pagina `/` respondendo `200`
- `npm run typecheck` (TypeScript) OK
- API local (`uvicorn`) integrada aos proxies Next

## Objetivo do proximo ciclo (Wave 2)

1. Refinar UX de operacao (empty states, loading states, mensagens de erro/sucesso)
2. Melhorar painel de `generation-jobs` (UX de lote e estados operacionais)
3. Extrair tipos/cliente API compartilhado (`web/lib/api-client.ts`)
4. Adicionar testes de UI (minimo smoke) e/ou E2E inicial (Playwright, quando priorizado)
5. Evoluir navegacao/layout (tabs/rotas) para reduzir rolagem na operacao

## Backlog UI sugerido (curto prazo)

1. Presets de filtros adicionais (`approved`, `published`)
2. Persistir preferencias adicionais de UI (colapso por painel / layout)
3. Colapsar secoes por painel (Gerar / Produtos / Jobs) com estado persistido
4. Evoluir presets operacionais para regras reais de negocio por squad
5. Estados vazios guiados (CTA para gerar primeiro produto / primeiro job)

## Dependencias

- API Wave 1 rodando localmente
- `NEXT_PUBLIC_API_BASE_URL` apontando para a API
