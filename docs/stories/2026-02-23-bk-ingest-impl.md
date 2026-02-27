# Story 1.4: Implement ingest pipeline CLI for base de conhecimento

**Epic:** Base Conhecimento
**Story ID:** 1.4
**Sprint:** 1
**Priority:** High
**Points:** 8
**Effort:** 8-10 hours
**Status:** Ready
**Type:** Feature

---

## Cross-Story Decisions

| Decision | Source | Impact on This Story |
|----------|--------|----------------------|
| Fluxo raw->extracao->normalizacao->markdown | Story 1.3 | Implementacao deve seguir o desenho |

---

## User Story

**Como** usuario do sistema,
**Quero** um CLI de ingestao para fontes brutas,
**Para** gerar markdown estruturado e classificado automaticamente.

---

## Objective

Implementar um pipeline CLI-first que:
- copia arquivos para `_raw`,
- extrai texto (pdf/html/txt),
- normaliza,
- gera markdown estruturado,
- classifica em `tecidos`, `modelagem`, `tecnologias`,
- encaminha casos ambíguos para `_pendente`.

---

## Tasks

### Phase 1: CLI (1h)

- [x] **1.1** Criar `pipeline/bk_ingest.py` com argparse

### Phase 2: Core logic (4h)

- [x] **2.1** Implementar extracao por tipo
- [x] **2.2** Implementar normalizacao
- [x] **2.3** Implementar markdown estruturado
- [x] **2.4** Implementar classificacao automatica

### Phase 3: Output (2h)

- [x] **3.1** Gravar arquivos em pastas corretas
- [x] **3.2** Atualizar file list

---

## Acceptance Criteria

```gherkin
GIVEN arquivos PDF, HTML e TXT
WHEN executar o CLI de ingestao
THEN deve gerar markdown estruturado por item
AND classificar em tecidos/modelagem/tecnologias
AND mover ambíguos para _pendente
```

---

## CodeRabbit Integration

### Story Type Analysis

| Attribute | Value | Rationale |
|-----------|-------|-----------|
| Type | Feature | Nova funcionalidade |
| Complexity | Medium | Pipeline com etapas |
| Test Requirements | Manual | Sem suite definida |
| Review Focus | Logic | Extracao e classificacao |

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
    - path: "pipeline/bk_ingest.py"
      instructions: "Verify ingestion steps and classification."

chat:
  auto_reply: true
```

### Focus Areas

- [ ] Extracao de pdf/html/txt
- [ ] Markdown estruturado conforme template
- [ ] Classificacao automatica correta

---

## Dependencies

**Blocked by:**
- N/A

**Blocks:**
- Populacao automatica da base

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| PDF parsing limitado | Medium | Fallback e logs claros |

---

## Definition of Done

- [x] CLI implementado
- [x] Markdown estruturado gerado
- [x] Classificacao automatica funcionando
- [x] File list atualizada

---

## Dev Notes

### Key Files

```
pipeline/bk_ingest.py
```

### Technical Notes

- Sem dependencias externas obrigatorias.

### File List

- pipeline/bk_ingest.py
- docs/stories/2026-02-23-bk-ingest-impl.md

### Testing Checklist

#### Manual
- [ ] Rodar com um arquivo TXT de exemplo

---

## Dev Agent Record

> This section is populated when @dev executes the story.

### Execution Log

| Timestamp | Phase | Action | Result |
|-----------|-------|--------|--------|
| 2026-02-23 | Story setup | Created story | Done |
| 2026-02-23 | Ingest CLI | Implemented pipeline/bk_ingest.py | Done |

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
**Atualizado:** 2026-02-23 (Ingest CLI implemented)
