# Story 1.11: Evoluir validador de BK para qualidade de conteudo

**Epic:** Base Conhecimento
**Story ID:** 1.11
**Sprint:** 1
**Priority:** Medium
**Points:** 5
**Effort:** 4-6 hours
**Status:** Ready
**Type:** Validation

---

## Cross-Story Decisions

| Decision | Source | Impact on This Story |
|----------|--------|----------------------|
| BK precisa de validacao de qualidade e nao so estrutura | `docs/roadmap-proximos-passos.md` | Expandir `bk_validator` |

---

## User Story

**Como** owner do clone,
**Quero** validar qualidade dos markdowns da BK,
**Para** evitar que conteudo ruidoso degrade o gerador.

---

## Objective

Expandir `core/bk_validator.py` e `pipeline/bk_validate.py` para validar:
- estrutura,
- densidade minima de conteudo,
- presenca de sinais tecnicos,
- ruido excessivo.

---

## Tasks

### Phase 1: Regras (1.5h)

- [x] **1.1** Definir regras de qualidade (min chars, termos tecnicos, ruido)
- [x] **1.2** Definir severidades (erro/aviso)

### Phase 2: Implementacao (2h)

- [x] **2.1** Atualizar `core/bk_validator.py` com regras de qualidade
- [x] **2.2** Atualizar `pipeline/bk_validate.py` para reportar avisos e erros
- [x] **2.3** Tratar `## Sinais Tecnicos Extraidos` como secao opcional suportada

### Phase 3: Validacao (1h)

- [x] **3.1** Rodar em `base_conhecimento/`
- [x] **3.2** Confirmar que arquivos ruidosos sao sinalizados

---

## Acceptance Criteria

```gherkin
GIVEN markdowns estruturados da BK
WHEN executar bk_validate.py
THEN o validador deve apontar erros estruturais e sinais de baixa qualidade
AND suportar a secao opcional de sinais tecnicos
```

---

## CodeRabbit Integration

### Story Type Analysis

| Attribute | Value | Rationale |
|-----------|-------|-----------|
| Type | Validation | Qualidade da BK |
| Complexity | Medium | Regras e report |
| Test Requirements | Manual | Base atual + casos ruidosos |
| Review Focus | Logic | Thresholds e falsos positivos |

### Agent Assignment

| Role | Agent | Responsibility |
|------|-------|----------------|
| Primary | @dev | Implementacao |
| Secondary | @qa | Revisao posterior |
| Review | @qa | Validacao |

### Self-Healing Config

```yaml
reviews:
  auto_review:
    enabled: true
    drafts: false
  path_instructions:
    - path: "core/bk_validator.py"
      instructions: "Verify quality heuristics and severity semantics."
    - path: "pipeline/bk_validate.py"
      instructions: "Verify report formatting and exit codes."

chat:
  auto_reply: true
```

### Focus Areas

- [x] Qualidade alem da estrutura
- [x] Thresholds praticos
- [x] Report util para limpeza

---

## Dependencies

**Blocked by:**
- N/A

**Blocks:**
- Operacao segura em escala da BK

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Falsos positivos em arquivos curtos validos | Medium | Threshold por categoria e avisos vs erros |

---

## Definition of Done

- [x] Validador de qualidade implementado
- [x] CLI reporta erros/avisos
- [x] Secao opcional suportada
- [x] File list atualizada

---

## Dev Notes

### Key Files

```
core/bk_validator.py
pipeline/bk_validate.py
```

### Testing Checklist

#### Manual
- [x] Rodar `python pipeline\\bk_validate.py --base base_conhecimento`
- [x] Verificar saida para arquivos de OCR e HTML concorrente

### File List

- core/bk_validator.py
- pipeline/bk_validate.py
- docs/stories/2026-02-24-bk-validator-quality.md

---

## Dev Agent Record

> This section is populated when @dev executes the story.

### Execution Log

| Timestamp | Phase | Action | Result |
|-----------|-------|--------|--------|
| 2026-02-24 | Story setup | Created story | Done |
| 2026-02-26 | Phase 1-2 | Implemented quality heuristics (errors/warnings) in BK validator and CLI report | Done |
| 2026-02-26 | Phase 3 | Ran validator on `base_conhecimento` and confirmed noisy files flagged | Done |

### Implementation Notes

- `core/bk_validator.py` foi refeito para:
  - validar estrutura por secoes (`## ...`)
  - suportar `## Sinais Tecnicos Extraidos` como secao opcional
  - aplicar heuristicas de qualidade (tamanho de `Detalhes`, resumo, termos tecnicos, ruido)
  - separar severidades em `errors` e `warnings`
  - retornar relatorio com `summary` + findings por arquivo
- `pipeline/bk_validate.py` agora:
  - imprime resumo agregado (arquivos, erros, avisos)
  - lista findings com prefixo `[ERRO]` / `[AVISO]`
  - retorna exit code `1` apenas quando ha erros
- Validacao em `base_conhecimento` sinalizou corretamente markdowns ruidosos antigos de Unbound Merino (`reviews/shipping`) e arquivos curtos de `_pendente`.

### Issues Encountered

Sem bloqueios de implementacao. Houve muitos findings na base atual, o que era esperado e util para limpeza.

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
