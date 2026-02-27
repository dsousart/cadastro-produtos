# Story 1.8: Hardening do clone e BK

**Epic:** Cadastro Premium
**Story ID:** 1.8
**Sprint:** 1
**Priority:** High
**Points:** 8
**Effort:** 8-10 hours
**Status:** Done
**Type:** Feature

---

## Cross-Story Decisions

| Decision | Source | Impact on This Story |
|----------|--------|----------------------|
| Estrutura do clone definida | Conversa externa | Atualizar SPEC e gerador |

---

## User Story

**Como** owner do produto,
**Quero** endurecer o clone e a BK,
**Para** garantir qualidade e consistencia no cadastro premium.

---

## Objective

Implementar:
- estrutura obrigatoria no cadastro,
- pipeline RAW -> EXTRAIDO -> MARKDOWN,
- BK reader com confidence_score,
- validador de BK,
- pacote inicial de BK.

---

## Tasks

### Phase 1: Spec e geracao (2h)

- [x] **1.1** Atualizar SPEC com estrutura obrigatoria e campos BK
- [x] **1.2** Atualizar generator/refiner para blocos obrigatorios

### Phase 2: Pipeline BK (3h)

- [x] **2.1** Criar raw_concorrentes/ e bk_extracted/
- [x] **2.2** Criar core/extract_raw.py
- [x] **2.3** Criar core/normalize_to_markdown.py

### Phase 3: Qualidade BK (2h)

- [x] **3.1** Atualizar bk_reader com confidence_score
- [x] **3.2** Ajustar auditor para penalizar baixa confianca
- [x] **3.3** Criar bk_validator e CLI de validacao

### Phase 4: Seed BK (1h)

- [x] **4.1** Criar arquivos iniciais de BK (tecidos/modelagem/tecnologias)
- [x] **4.2** Registrar analise e plano

---

## Acceptance Criteria

```gherkin
GIVEN uma ficha tecnica valida
WHEN executar o pipeline
THEN o texto deve conter blocos obrigatorios
AND a auditoria deve considerar confianca da BK
AND a BK deve passar na validacao basica
```

---

## CodeRabbit Integration

### Story Type Analysis

| Attribute | Value | Rationale |
|-----------|-------|-----------|
| Type | Feature | Melhorias de qualidade |
| Complexity | Medium | Multiplos modulos |
| Test Requirements | Manual | Sem suite definida |
| Review Focus | Logic | Regras e validacao |

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
    - path: "core/*.py"
      instructions: "Verify BK confidence and structure blocks."

chat:
  auto_reply: true
```

### Focus Areas

- [ ] Blocos obrigatorios no texto
- [ ] BK confidence e auditoria
- [ ] Validador de BK

---

## Dependencies

**Blocked by:**
- N/A

**Blocks:**
- Escala segura da BK

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Texto curto apos blocos | Medium | Refiner ajusta tamanhos |

---

## Definition of Done

- [x] SPEC atualizado
- [x] Blocos obrigatorios no output
- [x] Pipeline RAW/EXTRAIDO/MD criado
- [x] BK confidence e auditoria
- [x] Validador de BK
- [x] Seed BK criado
- [x] File list atualizada

---

## Dev Notes

### Key Files

```
SPEC.md
core/generator.py
core/refiner.py
core/bk_reader.py
core/auditor.py
core/extract_raw.py
core/normalize_to_markdown.py
core/bk_validator.py
pipeline/bk_validate.py
docs/clone-review-and-plan.md
```

### Testing Checklist

#### Manual
- [ ] Rodar pipeline com exemplo e validar blocos
- [ ] Rodar bk_validate

### File List

- SPEC.md
- docs/clone-review-and-plan.md
- raw_concorrentes/
- bk_extracted/
- core/generator.py
- core/refiner.py
- core/bk_reader.py
- core/auditor.py
- core/extract_raw.py
- core/normalize_to_markdown.py
- core/bk_validator.py
- pipeline/pipeline.py
- pipeline/run.py
- pipeline/bk_validate.py
- base_conhecimento/tecidos/algodao_egipcio.md
- base_conhecimento/tecidos/suedine.md
- base_conhecimento/tecidos/piquet.md
- base_conhecimento/tecnologias/pre_encolhido.md
- base_conhecimento/tecnologias/anti_pilling.md
- base_conhecimento/tecnologias/respirabilidade_absorcao.md
- base_conhecimento/modelagem/regular.md
- base_conhecimento/modelagem/slim.md
- docs/stories/2026-02-23-clone-hardening.md

---

## Dev Agent Record

> This section is populated when @dev executes the story.

### Execution Log

| Timestamp | Phase | Action | Result |
|-----------|-------|--------|--------|
| 2026-02-23 | Story setup | Created story | Done |
| 2026-02-23 | Implementation | Hardening completed | Done |

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
**Atualizado:** 2026-02-23 (Hardening completed)

