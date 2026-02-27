# Story 1.2: Add pipeline runner output adapter

**Epic:** Core Engine
**Story ID:** 1.2
**Sprint:** 1
**Priority:** Medium
**Points:** 3
**Effort:** 3-4 hours
**Status:** Ready
**Type:** Feature

---

## Cross-Story Decisions

| Decision | Source | Impact on This Story |
|----------|--------|----------------------|
| N/A | N/A | N/A |

---

## User Story

**Como** desenvolvedor,
**Quero** um runner dedicado do pipeline,
**Para** gerar um JSON simplificado para consumo externo.

---

## Objective

Criar `pipeline/run.py` com argparse para ler input, executar pipeline e exportar
os campos `texto_final`, `scores`, `melhorias_sugeridas`, `trechos_BK_usados`.

---

## Tasks

### Phase 1: Runner (2h)

- [x] **1.1** Implementar `pipeline/run.py`
- [x] **1.2** Atualizar file list da story

---

## Acceptance Criteria

```gherkin
GIVEN um JSON de entrada valido
WHEN executar pipeline/run.py com --input e --out
THEN o output deve conter texto_final, scores, melhorias_sugeridas, trechos_BK_usados
```

---

## CodeRabbit Integration

### Story Type Analysis

| Attribute | Value | Rationale |
|-----------|-------|-----------|
| Type | Feature | Runner de pipeline |
| Complexity | Low | Adaptacao de output |
| Test Requirements | Manual | Sem suite definida |
| Review Focus | Logic | Mapeamento de campos |

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
    - path: "pipeline/run.py"
      instructions: "Verify argparse and output mapping."

chat:
  auto_reply: true
```

### Focus Areas

- [ ] Output JSON conforme solicitado
- [ ] CLI com --input e --out

---

## Dependencies

**Blocked by:**
- N/A

**Blocks:**
- N/A

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Campo texto_final ambiguo | Low | Documentar composicao do texto |

---

## Definition of Done

- [x] `pipeline/run.py` criado
- [x] Output JSON valido
- [ ] Acceptance criteria verificado
- [x] File list atualizada

---

## Dev Notes

### Key Files

```
pipeline/run.py
```

### Technical Notes

- `texto_final` sera composto por titulo + subtitulo + descricao + bullets.

### File List

- pipeline/run.py
- examples-run-output.md
- docs/stories/2026-02-23-pipeline-run.md

### Testing Checklist

#### Manual
- [ ] Executar runner com exemplo

---

## Dev Agent Record

> This section is populated when @dev executes the story.

### Execution Log

| Timestamp | Phase | Action | Result |
|-----------|-------|--------|--------|
| 2026-02-23 | Story setup | Created story | Done |
| 2026-02-23 | Runner | Implemented pipeline/run.py | Done |

### Implementation Notes

_To be filled during execution._

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
| 2026-02-23 | 1.0.0 | Initial story creation | @dev |

---

**Criado por:** Codex (@dev)
**Data:** 2026-02-23
**Atualizado:** 2026-02-23 (Runner implemented)
