# Story 1.10: OCR seletivo por assets com texto tecnico

**Epic:** Base Conhecimento
**Story ID:** 1.10
**Sprint:** 1
**Priority:** High
**Points:** 3
**Effort:** 3-4 hours
**Status:** Ready
**Type:** Feature

---

## Cross-Story Decisions

| Decision | Source | Impact on This Story |
|----------|--------|----------------------|
| OCR deve ser opcional e com alto valor | `docs/roadmap-proximos-passos.md` | Filtrar assets antes de OCR |

---

## User Story

**Como** owner da BK,
**Quero** rodar OCR apenas em imagens com alta chance de conter texto tecnico,
**Para** reduzir ruido e custo de processamento.

---

## Objective

Adicionar filtros de assets para OCR em `core/extract_raw.py` com heuristicas por nome de arquivo/path.

---

## Tasks

### Phase 1: Heuristicas (1h)

- [x] **1.1** Definir allowlist de nomes (`feature`, `benefit`, `materials`, `fabric`)
- [x] **1.2** Definir denylist (`gallery`, `model`, `product`, `thumbnail`)

### Phase 2: Implementacao (1.5h)

- [x] **2.1** Aplicar filtro antes de `_extract_image_ocr`
- [x] **2.2** Logar contagem de assets elegiveis vs descartados (stdout simples)

### Phase 3: Validacao (0.5h)

- [x] **3.1** Rodar extração OCR no HTML salvo
- [x] **3.2** Verificar queda de arquivos OCR inuteis

---

## Acceptance Criteria

```gherkin
GIVEN uma pasta *_files com imagens de produto e banners
WHEN executar extract_raw.py com --ocr
THEN o OCR deve processar apenas assets elegiveis
AND reduzir geracao de txt de baixo valor
```

---

## CodeRabbit Integration

### Story Type Analysis

| Attribute | Value | Rationale |
|-----------|-------|-----------|
| Type | Feature | Otimizacao de OCR |
| Complexity | Low | Heuristicas por nome |
| Test Requirements | Manual | Pasta de assets existente |
| Review Focus | Logic | Filtros e falso-negativo |

### Agent Assignment

| Role | Agent | Responsibility |
|------|-------|----------------|
| Primary | @dev | Implementacao |
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
      instructions: "Verify OCR asset filtering heuristics and fallback."

chat:
  auto_reply: true
```

### Focus Areas

- [x] Allowlist/denylist de assets
- [x] Reducao de ruido OCR

---

## Dependencies

**Blocked by:**
- Tesseract OCR funcional

**Blocks:**
- Escala de OCR em concorrentes

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Perder imagem util por filtro agressivo | Medium | Allowlist/denylist configuravel |

---

## Definition of Done

- [x] Filtro de assets OCR implementado
- [x] Teste manual concluido
- [x] File list atualizada

---

## Dev Notes

### Key Files

```
core/extract_raw.py
```

### Testing Checklist

#### Manual
- [x] Rodar `extract_raw.py --ocr` em `raw_concorrentes`
- [x] Contar `.txt` de OCR gerados

### File List

- core/extract_raw.py
- docs/stories/2026-02-24-bk-ocr-asset-filter.md

---

## Dev Agent Record

> This section is populated when @dev executes the story.

### Execution Log

| Timestamp | Phase | Action | Result |
|-----------|-------|--------|--------|
| 2026-02-24 | Story setup | Created story | Done |
| 2026-02-26 | Phase 1-2 | Added OCR asset allowlist/denylist + stdout counters | Done |
| 2026-02-26 | Phase 3 | Ran `extract_raw.py --ocr` and validated eligibility reduction | Done |

### Implementation Notes

- Heuristicas por nome/path adicionadas em `core/extract_raw.py`.
- Allowlist inclui termos de maior probabilidade tecnica (`benefit`, `fabric`, `care`, `material`, `wool`, `micron`).
- Denylist remove assets comuns de ruido (`thumbnail`, `logo`, `testimonial`, `menu`, `lifestyle`, etc.).
- Filtro aplicado antes de chamar `_extract_image_ocr`, reduzindo processamento desnecessario.
- `run_extract()` agora imprime contagem: `OCR assets: elegiveis=X descartados=Y`.
- Validacao em `raw_concorrentes` (amostra Unbound Merino): 68 imagens totais, 8 elegiveis, 60 descartadas.
- Observacao: OCR real depende de PIL/pytesseract/Tesseract no ambiente; a validacao desta story confirmou a etapa de selecao.

### Issues Encountered

Nenhum bloqueio na implementacao do filtro. OCR efetivo continua dependente do ambiente local (libs + Tesseract).

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
