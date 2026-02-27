# Story 1.5: Implement CLI scraper para fontes web

**Epic:** Base Conhecimento
**Story ID:** 1.5
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
| Ingest pipeline definido | Story 1.3 | Scraper deve alimentar o ingest |

---

## User Story

**Como** usuario do sistema,
**Quero** um scraper CLI-first,
**Para** coletar paginas masculinas de concorrentes e alimentar a base de conhecimento.

---

## Objective

Implementar um CLI que:
- respeite robots.txt,
- limite paginas por dominio (200-500),
- filtre paginas masculinas (men/masculino),
- baixe HTML e salve em `_raw_web`,
- opcionalmente acione ingest do conteudo.

---

## Tasks

### Phase 1: CLI (1h)

- [x] **1.1** Criar `pipeline/bk_scraper.py` com argparse

### Phase 2: Core logic (5h)

- [x] **2.1** Implementar crawler por dominio com limite
- [x] **2.2** Implementar filtro masculino e exclusoes
- [x] **2.3** Respeitar robots.txt e rate limit
- [x] **2.4** Salvar HTML bruto

### Phase 3: Integration (2h)

- [x] **3.1** Integrar com `pipeline/bk_ingest.py` (opcional)
- [x] **3.2** Atualizar file list

---

## Acceptance Criteria

```gherkin
GIVEN um arquivo de configuracao com dominios
WHEN executar o scraper
THEN deve baixar ate N paginas por dominio
AND respeitar robots.txt
AND filtrar paginas masculinas
```

---

## CodeRabbit Integration

### Story Type Analysis

| Attribute | Value | Rationale |
|-----------|-------|-----------|
| Type | Feature | Nova funcionalidade |
| Complexity | Medium | Crawler e filtros |
| Test Requirements | Manual | Sem suite definida |
| Review Focus | Logic | Crawling e limites |

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
    - path: "pipeline/bk_scraper.py"
      instructions: "Verify robots compliance and limits."

chat:
  auto_reply: true
```

### Focus Areas

- [ ] Robots.txt
- [ ] Limite por dominio
- [ ] Filtro masculino

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
| Bloqueio por sites | Medium | Rate limit e user-agent |

---

## Definition of Done

- [x] CLI implementado
- [x] Respeito a robots e limites
- [x] Filtro masculino funcional
- [x] File list atualizada

---

## Dev Notes

### Key Files

```
pipeline/bk_scraper.py
```

### Testing Checklist

#### Manual
- [ ] Rodar com 1 dominio e limite 5

### File List

- pipeline/bk_scraper.py
- docs/scraper-sources.txt
- docs/scraper-sources-test.txt
- docs/stories/2026-02-23-bk-scraper-impl.md

---

## Dev Agent Record

> This section is populated when @dev executes the story.

### Execution Log

| Timestamp | Phase | Action | Result |
|-----------|-------|--------|--------|
| 2026-02-23 | Story setup | Created story | Done |
| 2026-02-23 | Scraper | Implemented pipeline/bk_scraper.py | Done |

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
**Atualizado:** 2026-02-23 (Scraper implemented)
