# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

# Cadastro de Produtos Premium - Moda Masculina 30+

Este é um projeto Python que automatiza o cadastro premium de produtos de moda masculina para público 30+, garantindo consistência de marca, padronização de atributos e qualidade editorial com auditoria rastreável.

## Arquitetura do Sistema

### Pipeline de Processamento

O sistema segue um pipeline de 7 etapas principais:

1. **Ingestão** → Valida campos obrigatórios e tipos
2. **Normalização** → Padroniza tamanhos, cores e composição
3. **Enriquecimento** → Sugere atributos derivados
4. **Copy Premium** → Gera título, subtítulo, descrição e bullets
5. **Revisão** → Valida diretrizes da marca
6. **SEO** → Gera meta title, description e slug
7. **Score e Auditoria** → Calcula score de qualidade (0-100)

### Estrutura de Diretórios

```
.
├── core/                    # Módulos principais do pipeline
│   ├── generator.py         # Geração de conteúdo premium
│   ├── auditor.py          # Auditoria e validação
│   ├── refiner.py          # Refinamento iterativo
│   ├── bk_reader.py        # Leitor de base de conhecimento
│   ├── bk_validator.py     # Validação de BK
│   ├── extract_raw.py      # Extração de conteúdo bruto
│   └── normalize_to_markdown.py  # Normalização para markdown
│
├── pipeline/               # Orquestração do pipeline
│   ├── pipeline.py         # Pipeline principal
│   ├── run.py             # Runner CLI
│   ├── bk_ingest.py       # Ingestão de BK
│   ├── bk_scraper.py      # Scraper de concorrentes
│   └── bk_validate.py     # Validação de BK
│
├── base_conhecimento/      # Base de conhecimento (marca, categoria, etc)
├── bk_extracted/          # Dados extraídos de concorrentes
├── raw_concorrentes/      # HTMLs brutos de scraping
├── docs/                  # Documentação e stories
│   └── stories/           # Stories de desenvolvimento
└── .aios-core/            # Framework Synkra AIOS
```

## Comandos Principais

### Pipeline de Cadastro

```bash
# Executar pipeline completo (geração + auditoria + refinamento)
python pipeline/run.py --input examples-input.json --out output.json

# Especificar caminho da base de conhecimento
python pipeline/run.py --input produto.json --out output.json --bk ./base_conhecimento

# Limitar iterações de refinamento (padrão: 2)
python pipeline/run.py --input produto.json --out output.json --max-iterations 3
```

### Pipeline Alternativo (sem refinamento)

```bash
# Executar apenas geração e auditoria
python pipeline/pipeline.py --input produto.json --output resultado.json
```

### Base de Conhecimento

```bash
# Scraping de concorrentes (com browser headless)
python pipeline/bk_scraper.py --sources docs/scraper-sources.txt --output raw_concorrentes/

# Extrair conteúdo dos HTMLs brutos para markdown
python core/extract_raw.py --input raw_concorrentes/ --output bk_extracted/

# Normalizar markdown extraído
python core/normalize_to_markdown.py --input bk_extracted/ --output base_conhecimento/

# Ingestão completa de BK (scraping + extração + normalização)
python pipeline/bk_ingest.py --sources docs/scraper-sources.txt --output base_conhecimento/

# Validar qualidade da base de conhecimento
python pipeline/bk_validate.py --bk-dir base_conhecimento/
```

## Especificação do Produto (SPEC.md)

O arquivo `SPEC.md` define as regras de entrada, saída e validação:

### Entradas Obrigatórias
- `sku`, `nome_produto`, `descricao_bruta`, `marca`, `categoria`
- `tamanhos`, `cores`, `preco`, `imagens`
- `guidelines_marca`, `regras_categoria`, `restricoes_legais`

### Saídas Geradas
- **Conteúdo**: `titulo`, `subtitulo`, `descricao`, `bullet_points`
- **Estrutura**: `blocos` (headline, abertura, benefícios, autoridade, uso, risco)
- **Metadata**: `atributos_normalizados`, `tags`, `seo`
- **Qualidade**: `score_qualidade` (0-100), `auditoria`, `bk_context`

### Score de Qualidade (0-100)
- Dados obrigatórios: 25 pontos
- Conteúdo premium: 25 pontos
- Conformidade marca/legal: 20 pontos
- SEO: 10 pontos
- Imagens: 10 pontos
- Consistência de atributos: 10 pontos

## Fluxo de Desenvolvimento

### Story-Driven Development (AIOS)

1. **Trabalhe a partir de stories** em `docs/stories/`
2. **Marque progresso** com checkboxes: `[ ]` → `[x]`
3. **Atualize File List** na story ao modificar arquivos
4. **Siga acceptance criteria** exatamente como especificado

### Padrões de Código

- **Python 3.8+** com type hints
- Funções prefixadas com `_` são privadas/helpers
- Normalização: use `_normalize_list()`, `_unique()`, `_title_case()`
- Slugify: use `_slugify()` para URLs
- Leitura de JSON: use `_load_json()` e `_write_json()`

### Base de Conhecimento

A base de conhecimento é organizada por domínios:
- `base_conhecimento/{domain}/` - Um diretório por site
- Arquivos `.md` com conteúdo normalizado
- Metadata em frontmatter YAML (opcional)

**Validação de BK**:
```python
from core.bk_reader import read_base_conhecimento, build_context

bk_data = read_base_conhecimento("./base_conhecimento")
bk_context = build_context(product, bk_data)
```

## Testes e Validação

### Arquivos de Exemplo

- `examples-input.json` - Exemplo de produto de entrada
- `examples-output.json` - Saída esperada do pipeline
- `examples-run-output.json` - Saída formatada para apresentação

### Validação Manual

```bash
# Ver apenas scores e melhorias
cat examples-run-output.json | jq '.scores'

# Ver trechos de BK utilizados
cat examples-run-output.json | jq '.trechos_BK_usados'

# Ver texto final completo
cat examples-run-output.json | jq -r '.texto_final'
```

## Integração com AIOS

Este projeto usa Synkra AIOS como meta-framework para orquestração de agentes.

### Agent Activation (AIOS)

- Agentes: `@dev`, `@qa`, `@architect`, `@pm`, `@po`, `@sm`, `@analyst`, `@devops`
- Master: `@aios-master`
- Comandos: `*help`, `*create-story`, `*task`, `*exit`

### AIOS Framework Structure

Ver `.aios-core/` para:
- `development/agents/` - Personas de agentes
- `development/tasks/` - Workflows executáveis
- `product/templates/` - Templates de documentos

### Common AIOS Commands

```bash
# Development
npm run dev
npm test
npm run lint
npm run build

# AIOS Sync
npm run sync:ide
npm run validate:structure
npm run validate:agents
```

## Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```bash
# LLM Providers (opcional para geração de conteúdo)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
DEEPSEEK_API_KEY=

# Para scraping avançado
EXA_API_KEY=
```

## Regras de Negócio

### Público-Alvo: Masculino 30+

- Linguagem madura e objetiva, sem gírias juvenis
- Valoriza qualidade, durabilidade e versatilidade
- Destaque de acabamento, tecido e caimento

### Matriz de Auditoria

| Área | Severidade | Regra |
|------|-----------|-------|
| Dados obrigatórios | Alta | SKU, nome, categoria, preço, imagens presentes |
| Padronização | Média | Tamanhos e cores seguem dicionário |
| Conteúdo | Média | Título 55-70, subtítulo 90-130, descrição 600-900 chars |
| Marca | Alta | Tom de voz e termos proibidos respeitados |
| Legal | Alta | Sem claims proibidos |
| SEO | Baixa | Meta title ≤60, meta description 140-160 |

### Estrutura de Cadastro Premium

1. **Headline** - Categoria + diferencial
2. **Abertura** - Ocasião de uso e público
3. **Benefícios** - Técnica traduzida em benefício
4. **Autoridade** - Tecido, processo, qualidade
5. **Uso Inteligente** - Combinações, ocasiões
6. **Redução de Risco** - Medidas, cuidados, encolhimento

## Troubleshooting

### Pipeline falha com SKU duplicado
```python
# O pipeline mantém histórico de SKUs processados
# Reset manual: remova do set seen_skus ou reinicie o processo
```

### Base de conhecimento vazia
```bash
# Verifique se há arquivos .md em base_conhecimento/
ls -R base_conhecimento/

# Rode a ingestão completa
python pipeline/bk_ingest.py --sources docs/scraper-sources.txt --output base_conhecimento/
```

### Score baixo na auditoria
```bash
# Veja os motivos de reprovação
cat output.json | jq '.auditoria.motivos_reprovacao'

# Rode refinamento manual
python pipeline/run.py --input produto.json --out output.json --max-iterations 5
```

---

## Claude Code Specific Configuration

### Performance Optimization
- Prefira chamadas em lote quando possível
- Use execução paralela para operações independentes
- Cache dados acessados frequentemente durante a sessão

### Tool Usage Guidelines
- Use `Grep` para busca, nunca `grep` ou `rg` via Bash
- Use `Task` tool para operações multi-etapa
- Leia/escreva arquivos em lote
- Prefira editar arquivos existentes a criar novos

### Session Management
- Acompanhe progresso da story durante a sessão
- Atualize checkboxes após completar tasks
- Mantenha contexto da story atual
- Salve estado antes de operações longas

---

*Cadastro de Produtos Premium v1.0 - Powered by Synkra AIOS*
