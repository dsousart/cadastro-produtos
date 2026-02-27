# SPEC.md — Agente de Cadastro Premium (Moda Masculina 30+)

## Objetivo
Automatizar o cadastro premium de produtos de moda masculina para público 30+, garantindo consistência de marca, padronização de atributos e qualidade editorial com auditoria rastreável.

## Entradas
- `sku` (string, obrigatório)
- `nome_produto` (string, obrigatório)
- `descricao_bruta` (string, obrigatório)
- `marca` (string, obrigatório)
- `categoria` (enum, obrigatório)
- `subcategoria` (enum, opcional)
- `tamanhos` (array<string>, obrigatório)
- `cores` (array<string>, obrigatório)
- `composicao` (string, opcional)
- `tecido` (string, opcional)
- `modelagem` (enum, opcional)
- `acabamento` (string, opcional)
- `colecao` (string, opcional)
- `preco` (number, obrigatório)
- `promocao` (object, opcional)
- `imagens` (array<url>, obrigatório)
- `guidelines_marca` (object, obrigatório)
- `regras_categoria` (object, obrigatório)
- `restricoes_legais` (object, obrigatório)

## Saídas
- `titulo` (string, 55–70 caracteres)
- `subtitulo` (string, 90–130 caracteres)
- `descricao` (string, 600–900 caracteres)
- `bullet_points` (array<string>, 4–6 itens)
- `atributos_normalizados` (object)
- `tags` (array<string>)
- `seo` (object: `meta_title`, `meta_description`, `slug`)
- `score_qualidade` (0–100)
- `auditoria` (object)
- `blocos` (object: `headline`, `abertura`, `beneficios`, `autoridade`, `uso`, `risco`)
- `bk_context` (object: `confidence_score`, `hits`, `missing_terms`, `snippets`)

## Pipeline
1. **Ingestao**
   - Valida obrigatorios e tipos.
   - Rejeita SKU duplicado.
2. **Normalizacao**
   - Normaliza tamanhos, cores e composicao.
   - Padroniza medidas e unidades.
3. **Enriquecimento**
   - Sugere modelagem, ocasiao e estilo.
   - Gera tags e atributos derivados.
4. **Copy Premium**
   - Redige titulo, subtitulo, descricao e bullets.
   - Adapta tom de voz para masculino 30+.
5. **Revisao**
   - Checa diretrizes da marca.
   - Valida claims e restricoes legais.
6. **SEO**
   - Gera meta title, description e slug.
7. **Score e Auditoria**
   - Calcula score.
   - Registra rastreabilidade.

## Matriz de Auditoria
| Area                | Regra                                               | Severidade | Evidencia                                    |
|---------------------|------------------------------------------------------|------------|----------------------------------------------|
| Dados obrigatorios  | SKU, nome, categoria, preco, imagens presentes       | Alta       | Campos ausentes                              |
| Padronizacao        | Tamanhos e cores seguem dicionario                   | Media      | Valor fora da lista permitida                |
| Conteudo            | Titulo 55–70, subtitulo 90–130, descricao 600–900     | Media      | Contagem de caracteres                       |
| Marca               | Tom de voz e termos proibidos respeitados            | Alta       | Match de guidelines_marca                    |
| Legal               | Sem claims proibidos                                 | Alta       | Lista de termos restritos                    |
| SEO                 | Meta title <= 60, meta description 140–160           | Baixa      | Contagem de caracteres                       |
| Imagens             | Min 3 imagens, resolucao minima                      | Media      | Metadados das imagens                        |
| Preco/Promocao      | Preco valido, promocao consistente                   | Media      | Regras de precificacao e validade            |
| Duplicidade         | Nao duplicar nome + marca + atributos-chave          | Alta       | Comparacao de similaridade                   |
| Qualidade editorial | Ortografia e fluidez                                 | Baixa      | Resultado de corretor e heuristicas          |

## Regras do Publico 30+
- Linguagem madura e objetiva, sem gírias juvenis.
- Valoriza qualidade, durabilidade e versatilidade.
- Destaque de acabamento, tecido e caimento.

## Score de Qualidade (0–100)
- Dados obrigatorios: 25
- Conteudo premium: 25
- Conformidade marca/legal: 20
- SEO: 10
- Imagens: 10
- Consistencia atributos: 10

## Observabilidade
- `audit_id`
- `timestamp`
- `usuario`
- `versao_pipeline`
- `resultado` (aprovado/reprovado)
- `motivos_reprovacao`

## Estrutura Obrigatoria do Cadastro
- Headline estrategica (categoria + diferencial)
- Abertura contextual (ocasiao de uso e publico)
- Beneficios traduzidos (tecnica -> beneficio)
- Autoridade (tecido, processo, qualidade)
- Uso inteligente (combinacoes, ocasioes)
- Reducao de risco (medidas, cuidados, encolhimento)
