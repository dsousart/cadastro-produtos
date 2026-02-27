# Story 1.7: Add sitemap-based discovery to BK scraper

**Epic:** Base Conhecimento
**Story ID:** 1.7
**Sprint:** 1
**Priority:** High
**Points:** 5
**Effort:** 4-6 hours
**Status:** Ready
**Type:** Feature

---

## Cross-Story Decisions

| Decision | Source | Impact on This Story |
|----------|--------|----------------------|
| Scraper CLI implemented | Story 1.5 | Extend discovery |

---

## User Story

**Como** usuario do sistema,
**Quero** descobrir URLs via sitemap,
**Para** reduzir bloqueios e aumentar a cobertura masculina.

---

## Objective

Adicionar descoberta via sitemap ao `pipeline/bk_scraper.py` com fallback para crawl.

---

## Tasks

### Phase 1: Sitemap parsing (2h)

- [x] **1.1** Implementar leitura de sitemap.xml e sitemap_index.xml
- [x] **1.2** Filtrar URLs por include/exclude

### Phase 2: Integration (2h)

- [x] **2.1** Adicionar flag `--use-sitemaps`
- [x] **2.2** Atualizar report

### Phase 3: Docs (1h)

- [x] **3.1** Atualizar file list

---

## Acceptance Criteria

```gherkin
GIVEN um dominio com sitemap
WHEN executar o scraper com --use-sitemaps
THEN deve coletar URLs do sitemap e respeitar filtros
AND ainda respeitar robots.txt
```

---

## CodeRabbit Integration

### Story Type Analysis

| Attribute | Value | Rationale |
|-----------|-------|-----------|
| Type | Feature | Nova forma de descoberta |
| Complexity | Medium | Parsing + integração |
| Test Requirements | Manual | Sem suite definida |
| Review Focus | Logic | URLs e filtros |

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
      instructions: "Verify sitemap parsing and filters."

chat:
  auto_reply: true
```

### Focus Areas

- [ ] Sitemap discovery
- [ ] Filtros e robots

---

## Dependencies

**Blocked by:**
- N/A

**Blocks:**
- Aumento de cobertura automatizada

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Sitemap incompleto | Medium | Fallback para crawl |

---

## Definition of Done

- [x] Sitemap discovery implementado
- [x] Flag CLI adicionada
- [x] File list atualizada

---

## Dev Notes

### Key Files

```
pipeline/bk_scraper.py
```

### Testing Checklist

#### Manual
- [ ] Rodar com 1 dominio com sitemap

### File List

- pipeline/bk_scraper.py
- docs/stories/2026-02-23-bk-scraper-sitemaps.md

---

## Dev Agent Record

> This section is populated when @dev executes the story.

### Execution Log

| Timestamp | Phase | Action | Result |
|-----------|-------|--------|--------|
| 2026-02-23 | Story setup | Created story | Done |
| 2026-02-23 | Sitemaps | Implemented sitemap discovery | Done |

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
**Atualizado:** 2026-02-23 (Sitemaps implemented)
