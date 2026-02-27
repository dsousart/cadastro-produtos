# ADR-000: Alinhamento PRD ↔ Arquitetura (Kickoff Wave 1)

**Status:** Aceito
**Data:** 2026-02-26
**Autores:** @architect / revisao cruzada PRD-arquitetura

---

## Contexto

Na revisao cruzada entre `docs/prd.md` e `docs/architecture.md`, foram encontrados desalinhamentos que afetam diretamente o kickoff da Wave 1:

1. `CR4` com significado diferente entre PRD e Arquitetura
2. Auth/RBAC antecipado para Wave 1 na Arquitetura, mas previsto para Wave 4 no PRD
3. Naming/contrato de processamento (`batches` no PRD vs `generation-jobs` na Arquitetura)
4. Health endpoints (`/health` no PRD vs `/healthz` + `/readyz` na Arquitetura)

Sem esse alinhamento, o time pode implementar a Wave 1 com escopo, contrato e testes divergentes.

---

## Decisao (proposta conservadora)

### D1. Preservar `CR4` do PRD como requisito oficial

**Decisao proposta:**
- `CR4` oficial = **Python Version Compatibility (Python 3.14+)**, conforme `docs/prd.md`

**Ajuste complementar:**
- O conceito de "pipeline de 7 etapas inalterado" deve permanecer na Arquitetura, mas como:
- restricao arquitetural/compatibilidade operacional adicional
- ou novo item (`CR5`) se o PRD for atualizado formalmente

### D2. Manter Auth/RBAC fora da Wave 1 (como no PRD)

**Decisao proposta:**
- Wave 1 = Foundation (API + Core Integration) sem depender de JWT/RBAC
- Auth/RBAC permanecem na Wave 4 (PRD), com possibilidade de:
- protecao minima por rede/ambiente interno
- chave simples de ambiente temporaria (se estritamente necessario)

**Justificativa:**
- reduz risco e tempo de entrega da primeira onda
- respeita sequenciamento do PRD

### D3. Adotar `generation-jobs` como modelo-alvo, com compatibilidade de rollout

**Decisao proposta:**
- Modelo conceitual/canônico na Arquitetura: `generation-jobs`
- PRD (stories Wave 1) deve ser atualizado para refletir esse naming **ou**
- implementar aliases/compatibilidade temporaria na API durante transicao

**Diretriz de transicao:**
- evitar dois contratos publicos permanentes
- escolher naming final antes de congelar OpenAPI da Wave 1

### D4. Padronizar health endpoints em `/healthz` e `/readyz`

**Decisao proposta:**
- Padrão final: `GET /healthz` (liveness) e `GET /readyz` (readiness)
- Se necessario para compatibilidade de stories iniciais, manter `/health` temporariamente como alias

**Justificativa:**
- separa liveness/readiness de forma operacionalmente melhor
- já está incorporado na Arquitetura (deploy, observabilidade, smoke pos-deploy)

---

## Consequencias

### Positivas

- Kickoff da Wave 1 fica com escopo tecnico mais claro
- Contratos e testes ficam alinhados (principalmente health e jobs)
- Reduz risco de retrabalho em API/OpenAPI e testes de integracao

### Negativas / Custos

- Exige patch de alinhamento no PRD e/ou Arquitetura
- Pode demandar ajuste de stories Wave 1 (naming de endpoints/jobs)

---

## Alternativas Consideradas

### A1. Seguir PRD literalmente e ignorar Arquitetura

**Rejeitada**
- Perde melhorias operacionais importantes (`/readyz`, separacao de observabilidade)
- Mantem ambiguidades para jobs futuros

### A2. Seguir Arquitetura literalmente e antecipar Auth/RBAC para Wave 1

**Rejeitada (por ora)**
- Aumenta escopo/risco da Wave 1
- Diverge do PRD sem aprovacao formal

### A3. Congelar ambos e decidir durante implementacao

**Rejeitada**
- Empurra ambiguidade para o time de desenvolvimento
- Aumenta chance de retrabalho e criterios de aceite conflitantes

---

## Impacto em Artefatos (patches recomendados apos aprovacao)

### `docs/prd.md`
- ajustar stories/ACs para naming final de jobs (`batches` vs `generation-jobs`)
- atualizar health endpoint (`/health` vs `/healthz`/`/readyz`)
- revisar Success Criteria "MVP - Fase 1" se continuar ambiguo com 20 stories

### `docs/architecture.md`
- alinhar definicao de `CR4` com PRD (Python 3.14+)
- mover "pipeline de 7 etapas inalterado" para restricao adicional (fora de CR4)
- explicitar se `/health` e alias temporario ou removido
- explicitar se Wave 1 usa auth minima temporaria (sem antecipar Wave 4)

### `docs/stories/` (Wave 1)
- ajustar naming e ACs quando a decisao final de endpoint/jobs for aprovada

---

## Criterio de Aprovacao deste ADR

Este ADR pode ser marcado como **Aceito** quando houver acordo explicito de @architect + @po (e idealmente @dev) sobre:

1. significado final de `CR4`
2. escopo de auth na Wave 1
3. naming final do recurso de processamento (`batches` vs `generation-jobs`)
4. padrão de health endpoints
