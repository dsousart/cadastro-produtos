# Pipeline de Ingestao da Base de Conhecimento

## Objetivo
Definir um fluxo CLI-first para transformar fontes brutas (PDF, HTML, TXT, sites) em
markdown estruturado, higienizado e classificado em `tecidos`, `modelagem`, `tecnologias`.

## Escopo de Fontes
- PDF (catalogos, fichas tecnicas, manuais)
- HTML (paginas de referencia, artigos tecnicos)
- TXT (notas internas, listas de termos)
- Sites de concorrentes (apenas conteudo publico)

## Fluxo Macro
1. Raw
2. Extracao
3. Normalizacao
4. Markdown Estruturado
5. Classificacao Automatica
6. Revisao e Publicacao

## 1. Raw
**Entrada**
- Arquivos originais, sem alteracao.

**Saida**
- Arquivos preservados em `base_conhecimento/_raw/`.

**Regras**
- Nunca editar o arquivo raw.
- Nomear com timestamp e origem.

## 2. Extracao
**Entrada**
- Raw (PDF/HTML/TXT).

**Saida**
- Texto bruto em UTF-8.
- Metadados basicos: `fonte`, `data_coleta`, `tipo_arquivo`, `url` (quando houver).

**Regras**
- Remover apenas artefatos de formato (quebras incoerentes, headers repetidos).
- Preservar tabelas como texto tabular simples quando possivel.

## 3. Normalizacao
**Entrada**
- Texto bruto extraido.

**Saida**
- Texto limpo, padronizado e segmentado.

**Regras**
- Padronizar unidades (ex.: cm, g/m2, %).
- Normalizar termos comuns (ex.: "algodao cru" -> "algodao").
- Remover duplicacoes, trechos irrelevantes e propaganda.
- Identificar entidades-chave: `tecido`, `modelagem`, `tecnologia`, `composicao`, `acabamento`.

## 4. Markdown Estruturado
**Entrada**
- Texto normalizado.

**Saida**
- Markdown seguindo `base_conhecimento/_TEMPLATE.md`.

**Campos minimos**
- `Titulo`
- `Categoria`
- `Fonte`
- `Data`
- `Resumo`
- `Detalhes`
- `Aplicacao no Cadastro`
- `Termos e Sinonimos`
- `Regras e Restricoes`
- `Tags`

## 5. Classificacao Automatica
**Entrada**
- Markdown estruturado.

**Saida**
- Pasta de destino: `tecidos`, `modelagem`, `tecnologias`.

**Estrategia**
1. **Regras (alta precisao)**. Se houver `Categoria` preenchida no markdown, usar como fonte primaria.
2. **Palavras-chave fortes**. Tecidos: algodao, linho, wool, sarja, oxford, malha, denim. Modelagem: slim, regular, oversized, alfaiataria, caimento. Tecnologias: repelencia, dry, termico, stretch, anti-odor, UV.
3. **Heuristicas (media precisao)**. Densidade de termos por paragrafo e presenca de unidades e especificacoes tecnicas.
4. **Fallback (baixa precisao)**. Se empate, mover para `base_conhecimento/_pendente/`.

## 6. Revisao e Publicacao
**Entrada**
- Arquivo classificado.

**Saida**
- Arquivo validado e aprovado para uso no pipeline.

**Regras**
- Conferir consistencia de termos e sinonimos.
- Validar ausencia de claims proibidos.

## Saidas Esperadas
- Markdown estruturado por item em `base_conhecimento/{categoria}/`.
- Trilhas de auditoria por item (metadados no arquivo).

## Exemplo de Arquivo Estruturado
```markdown
# TEMPLATE — Base de Conhecimento

## Titulo
Oxford 100% algodao

## Categoria
- tecidos

## Fonte
- https://exemplo.com/tecido-oxford

## Data
- 2026-02-23

## Resumo
- Tecido de algodao com trama mais fechada.
- Toque estruturado e boa durabilidade.

## Detalhes
- Utilizado em camisas sociais e casuais.
- Gramatura media e respirabilidade adequada.

## Aplicacao no Cadastro
- Usar em descricoes que precisem destacar estrutura e durabilidade.

## Termos e Sinonimos
- oxford, algodao penteado, tecido estruturado

## Regras e Restricoes
- Evitar claims absolutos como "indestrutivel".

## Tags
- #tecido #oxford #algodao
```
