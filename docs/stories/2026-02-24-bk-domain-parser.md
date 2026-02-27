# Story 1.9: Parser por dominio para extracao de blocos tecnicos

**Epic:** Base Conhecimento
**Story ID:** 1.9
**Sprint:** 1
**Priority:** High
**Points:** 5
**Effort:** 5-7 hours
**Status:** Ready
**Type:** Feature

---

## Cross-Story Decisions

| Decision | Source | Impact on This Story |
|----------|--------|----------------------|
| Foco em precisao de ingestao antes de volume | `docs/roadmap-proximos-passos.md` | Parser por dominio e prioridade |

---

## User Story

**Como** owner do clone de cadastro,
**Quero** extrair blocos tecnicos por dominio com maior precisao,
**Para** alimentar a BK com conteudo util e menos ruido.

---

## Objective

Implementar parser por dominio em `core/extract_raw.py` (ou modulo auxiliar) para capturar blocos relevantes de paginas de produto, iniciando por `unboundmerino`.

---

## Tasks

### Phase 1: Estrutura (1h)

- [x] **1.1** Definir mapa de seletores por dominio (`domain -> selectors`)
- [x] **1.2** Integrar escolha de parser no fluxo de HTML

### Phase 2: Implementacao (3h)

- [x] **2.1** Implementar parser `unboundmerino` (fabric/details/benefits/care)
- [x] **2.2** Fallback para extracao generica quando seletor falhar
- [x] **2.3** Preservar compatibilidade com fluxo atual

### Phase 3: Validacao (1h)

- [x] **3.1** Reprocessar HTML salvo do Unbound Merino
- [x] **3.2** Comparar tamanho e densidade de sinal tecnico antes/depois

---

## Acceptance Criteria

```gherkin
GIVEN um HTML salvo de produto do dominio unboundmerino
WHEN executar a extracao RAW
THEN a saida deve conter blocos tecnicos relevantes
AND reduzir ruido de menu/reviews/footer
AND manter fallback generico para outros dominios
```

---

## CodeRabbit Integration

### Story Type Analysis

| Attribute | Value | Rationale |
|-----------|-------|-----------|
| Type | Feature | Melhoria de extracao |
| Complexity | Medium | Seletores + fallback |
| Test Requirements | Manual | HTML salvo de referencia |
| Review Focus | Logic | Seletores e degradacao |

### Agent Assignment

| Role | Agent | Responsibility |
|------|-------|----------------|
| Primary | @dev | Implementar parser |
| Secondary | @qa | Revisao posterior |
| Review | @qa | Validacao manual |

### Self-Healing Config

```yaml
reviews:
  auto_review:
    enabled: true
    drafts: false
  path_instructions:
    - path: "core/extract_raw.py"
      instructions: "Verify domain-specific parser and generic fallback."

chat:
  auto_reply: true
```

### Focus Areas

- [x] Seletor por dominio
- [x] Fallback generico
- [x] Reducao de ruido

---

## Dependencies

**Blocked by:**
- N/A

**Blocks:**
- Qualidade da BK em paginas de concorrentes

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Mudanca de HTML no dominio | Medium | Fallback generico + mapa de seletores versionado |

---

## Definition of Done

- [x] Parser por dominio implementado para `unboundmerino`
- [x] Fallback preservado
- [x] HTML de teste reprocessado
- [x] File list atualizada

---

## Dev Notes

### Key Files

```
core/extract_raw.py
docs/roadmap-proximos-passos.md
```

### Testing Checklist

#### Manual
- [x] Rodar `extract_raw.py` no HTML salvo do Unbound Merino
- [x] Inspecionar `bk_extracted/*.txt`

### File List

- core/extract_raw.py
- docs/stories/2026-02-24-bk-domain-parser.md

---

## Dev Agent Record

> This section is populated when @dev executes the story.

### Execution Log

| Timestamp | Phase | Action | Result |
|-----------|-------|--------|--------|
| 2026-02-24 | Story setup | Created story | Done |
| 2026-02-26 | Phase 1-2 | Added domain parser (`unboundmerino`) + generic fallback | Done |
| 2026-02-26 | Phase 3 | Reprocessed saved HTML and compared output size/noise | Done |

### Implementation Notes

- Domain detection integrated in `core/extract_raw.py` HTML extraction path.
- `unboundmerino` parser extracts: description, feature badges, fit tab, fabric/details tab, care tab.
- Fallback generic extraction preserved when parser returns conteudo insuficiente.
- Comparacao manual (same HTML): generic ~28896 chars vs domain parser ~692 chars, removendo ocorrencias de `reviews` (40 -> 0) e `shipping` (18 -> 0) enquanto preserva sinais tecnicos (`190gsm`, `17.5 µm`, cuidados).

### Issues Encountered

_None yet - story not started._

---

## QA Results

> This section is populated after @qa reviews the implementation.

### Test Execution Summary

| Category | Tests | Passed | Failed | Skipped |
|----------|-------|--------|--------|---------|
| Unit | - | - | - | - |
| Integration | - | - | - | - |
| E2E | - | - | - | - |

### Validation Checklist

| Check | Status | Notes |
|-------|--------|-------|
| Acceptance criteria | Pending | |
| DoD items | Pending | |
| Edge cases | Pending | |
| Documentation | Pending | |

### QA Sign-off

- [ ] All acceptance criteria verified
- [ ] Tests passing (coverage >= 80%)
- [ ] Documentation complete
- [ ] Ready for release

**QA Agent:** _Awaiting assignment_
**Date:** _Pending_

---

## Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-02-24 | 1.0.0 | Initial story creation | @dev |

---

**Criado por:** Codex (@dev)
**Data:** 2026-02-24
**Atualizado:** 2026-02-24 (Story created)
