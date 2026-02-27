# Story - Wave 4 Web UX User-First Review

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Revisar a experiencia de uso das telas `Gerar`, `Produtos` e `Jobs` com foco em usuario final.
- Melhorar clareza de linguagem, fluxo de acao e feedback operacional.
- Garantir que a interface seja funcional para uso real, nao apenas tecnicamente correta.

## Objetivo

Elevar a usabilidade do workspace operacional para reduzir friccao no uso diario, tornar erros acionaveis e deixar os proximos passos sempre claros para o usuario.

## Checklist

- [x] Mapear principais jornadas do usuario (`Gerar -> Jobs -> Produtos`, consulta e revisao)
- [x] Identificar pontos de confusao de texto/acao por tela
- [x] Padronizar mensagens de sucesso/erro com linguagem simples e objetiva
- [x] Melhorar estados vazios com CTA claro para proximo passo
- [x] Revisar hierarquia visual das acoes principais vs secundarias
- [x] Validar consistencia de feedback (loading, erro, sucesso)
- [x] Executar validacao manual das jornadas apos ajustes
- [x] Executar `npm run lint`
- [x] Executar `npm run typecheck`
- [x] Executar `npm test`

## Acceptance Criteria

```gherkin
GIVEN um usuario final operando o workspace web
WHEN ele executar os fluxos principais de geracao e consulta
THEN cada tela deve deixar claro o que fazer em seguida
AND mensagens de erro devem indicar causa e acao recomendada
AND estados vazios devem conter CTA util para continuar o fluxo
AND a navegacao entre abas deve manter contexto operacional
```

## File List

- `web/components/product-generator-form.tsx`
- `web/components/products-list-panel.tsx`
- `web/components/generation-jobs-panel.tsx`
- `web/components/wave2-dashboard.tsx`
- `web/lib/api-client.ts`
- `docs/stories/2026-02-27-wave4-web-ux-user-first-review.md`

## DoD

- [x] UX revisada com foco em usuario final nas telas principais
- [x] Fluxos operacionais testados manualmente sem ambiguidade de acao
- [x] Quality gates (`lint`, `typecheck`, `test`) executados e verdes
- [x] Story atualizada com checklist e file list final

## Evidencias

- `npm run lint` (web) OK
- `npm run typecheck` (web) OK
- `npm test` (web) OK (16/16)
- Validacao manual local confirmada nas jornadas:
  - `Gerar -> Produtos` (persistencia e listagem)
  - `Jobs -> Produtos` (redirecionamento com foco)
  - `Produtos` com tratamento claro de erro `503` (CTA para Health)
