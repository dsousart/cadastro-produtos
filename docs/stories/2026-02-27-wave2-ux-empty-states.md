# Story - Wave 2 UX Empty States

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Guiar operador quando nao ha dados em `Produtos`
- Guiar operador quando nenhum `generation-job` foi iniciado
- Padronizar bloco visual de estado vazio com CTA direta

## Checklist

- [x] Produtos: estado vazio com orientacao contextual
- [x] Produtos: CTA para limpar filtros e ir para `Gerar`
- [x] Jobs: estado inicial com orientacao e CTA de primeiro job
- [x] Jobs: CTA para restaurar payload base
- [x] Estilo compartilhado para empty state adicionado
- [x] `npm run lint` executado
- [x] `npm run typecheck` executado

## Evidencias

- `cd web && npm run lint`
- `cd web && npm run typecheck`

## File List

- `web/components/products-list-panel.tsx`
- `web/components/generation-jobs-panel.tsx`
- `web/app/globals.css`

## DoD

- [x] Operacao sem tela vazia "morta" nos fluxos principais
- [x] Qualidade estatica (lint/typecheck) sem regressao
- [x] Story documentada com checklist e arquivos alterados
