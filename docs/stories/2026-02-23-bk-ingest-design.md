# Story 1.3: Design pipeline de ingestao e classificacao da base de conhecimento

**Epic:** Base Conhecimento
**Story ID:** 1.3
**Sprint:** 1
**Priority:** High
**Points:** 5
**Effort:** 5-7 hours
**Status:** Ready
**Type:** Documentation

---

## Cross-Story Decisions

| Decision | Source | Impact on This Story |
|----------|--------|----------------------|
| N/A | N/A | N/A |

---

## User Story

**Como** owner do produto,
**Quero** um fluxo claro de ingestao e higienizacao da base de conhecimento,
**Para** transformar fontes brutas em markdown estruturado e classificado.

---

## Objective

Desenhar o pipeline raw -> extracao -> normalizacao -> markdown estruturado e a
estrategia de classificacao automatica (tecidos, modelagem, tecnologias).

---

## Tasks

### Phase 1: Discovery (1h)

- [x] **1.1** Levantar fontes suportadas e requisitos de entrada/saida

### Phase 2: Design (3h)

- [x] **2.1** Definir etapas do pipeline e responsabilidades
- [x] **2.2** Definir schema de markdown estruturado
- [x] **2.3** Definir estrategia de classificacao automatica

### Phase 3: Delivery (1h)

- [x] **3.1** Documentar fluxo e exemplos
- [x] **3.2** Atualizar file list

---

## Acceptance Criteria

```gherkin
GIVEN fontes brutas (pdf, html, txt)
WHEN o fluxo for definido
THEN deve existir um pipeline claro com entradas/saidas e normalizacao
AND o metodo de classificacao por categoria deve estar descrito
```

---

## CodeRabbit Integration

### Story Type Analysis

| Attribute | Value | Rationale |
|-----------|-------|-----------|
| Type | Documentation | Desenho do fluxo |
| Complexity | Medium | Multiplas etapas e criterios |
| Test Requirements | Manual | N/A |
| Review Focus | Documentation | Clareza e completude |

### Agent Assignment

| Role | Agent | Responsibility |
|------|-------|----------------|
| Primary | @dev | Desenho do fluxo |
| Secondary | @qa | Revisao posterior |
| Review | @qa | Validacao |

### Self-Healing Config

```yaml
reviews:
  auto_review:
    enabled: true
    drafts: false
  path_instructions:
    - path: "docs/**/*.md"
      instructions: "Verify completeness and adherence to SPEC."

chat:
  auto_reply: true
```

### Focus Areas

- [ ] Pipeline raw->extracao->normalizacao->markdown
- [ ] Classificacao automatica
- [ ] Exemplos claros

---

## Dependencies

**Blocked by:**
- N/A

**Blocks:**
- Implementacao do ingest pipeline

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Ambiguidade de categorias | Medium | Regras + heuristicas + fallback manual |

---

## Definition of Done

- [x] Fluxo documentado
- [x] Estrutura de markdown definida
- [x] Classificacao descrita
- [x] File list atualizada

---

## Dev Notes

### Key Files

```
docs/bk-ingest.md
```

### Technical Notes

- Sem implementacao de codigo nesta story.

### File List

- docs/bk-ingest.md
- docs/stories/2026-02-23-bk-ingest-design.md

### Testing Checklist

#### Manual
- [ ] Revisar se o fluxo cobre pdf/html/txt

---

## Dev Agent Record

> This section is populated when @dev executes the story.

### Execution Log

| Timestamp | Phase | Action | Result |
|-----------|-------|--------|--------|
| 2026-02-23 | Story setup | Created story | Done |
| 2026-02-23 | Design | Documented ingest pipeline | Done |

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
**Atualizado:** 2026-02-23 (Pipeline documented)
