# Roadmap de Proximos Passos (Execucao de Amanha)

## Estado Atual (Consolidado)

### O que ja funciona
- Pipeline de cadastro premium (`core/generator.py`, `core/auditor.py`, `core/refiner.py`, `pipeline/pipeline.py`, `pipeline/run.py`)
- BK com template e seeds iniciais (tecidos/modelagem/tecnologias)
- Pipeline de ingestao (`core/extract_raw.py`, `core/normalize_to_markdown.py`)
- Leitura de BK com contexto (`confidence_score`, `hits`, `missing_terms`, `snippets`)
- Auditoria com penalizacao por baixa confianca da BK e ausencia de blocos obrigatorios
- Scraper com filtros masculinos, robots, relatorio e sitemap discovery
- OCR opcional em imagens com Tesseract via caminho explicito (`--tesseract-cmd`)

### O que foi validado hoje
- Extracao de HTML principal salvo do navegador (Unbound Merino)
- Ignorar HTMLs auxiliares da pasta `*_files` quando existe HTML principal
- OCR funcionando com `C:\\Program Files\\Tesseract-OCR\\tesseract.exe`
- Filtro de OCR inutil (nao gera `.txt` para textos curtos sem valor)
- Normalizacao gerando markdown com `## Sinais Tecnicos Extraidos`

### Limites atuais observados
- HTML salvo vem com muito ruido (menu, reviews, footer), mesmo com filtros gerais
- OCR em imagens traz resultados mistos (algumas imagens com texto tecnico, outras ruido)
- Classificacao por heuristica ainda e muito generica para sites de e-commerce complexos
- Validador BK atual nao conhece seções opcionais/novas e nao mede qualidade de conteudo

## Analise Tecnica (Diretiva)

### Problema principal agora
O gargalo nao e "extrair qualquer texto"; e "extrair texto certo com densidade tecnica alta".

### Consequencia pratica
Se a BK crescer com ruido:
- `bk_context.confidence_score` pode subir artificialmente
- o gerador passa a usar snippets fracos
- a auditoria perde sinal de qualidade real

### Decisao recomendada
Amanha focar em **precisao de ingestao**, nao em volume.

Ordem recomendada:
1. Parser por dominio (comecando por `unboundmerino`)
2. Filtro de OCR por assets "provavelmente textuais"
3. Validador BK de qualidade (nao so estrutura)

## Proximos Passos (Execucao)

### 1. Parser por dominio (alta prioridade)
Objetivo:
- extrair apenas blocos relevantes (`fabric/details`, `care`, `features`, `benefits`)
- reduzir drasticamente ruido

Resultado esperado:
- markdowns menores, mais tecnicos e mais uteis para cadastro premium

### 2. OCR com seletor de assets (alta prioridade)
Objetivo:
- processar OCR apenas em imagens com nome/URL de "feature/benefit/material"
- ignorar fotos de produto/galeria

Resultado esperado:
- menos arquivos OCR inutil
- maior taxa de sinais tecnicos aproveitaveis

### 3. Validador BK de qualidade (media prioridade)
Objetivo:
- validar estrutura + densidade minima de sinal tecnico + qualidade textual
- marcar arquivos para `_pendente` quando muito fracos

Resultado esperado:
- BK mais confiavel para o clone

## Checklist de Execucao de Amanha
- Rodar parser por dominio com 1 HTML salvo (Unbound Merino)
- Rodar normalizacao e inspecionar `Sinais Tecnicos Extraidos`
- Rodar OCR filtrado em assets
- Rodar `pipeline/bk_validate.py`
- Ajustar thresholds com base nos outputs reais

## Comandos Base (Amanha)
```powershell
python core\extract_raw.py --input "raw_concorrentes" --out "bk_extracted" --ocr --ocr-lang eng --tesseract-cmd "C:\Program Files\Tesseract-OCR\tesseract.exe"
python core\normalize_to_markdown.py --input "bk_extracted" --out "base_conhecimento" --source "concorrente"
python pipeline\bk_validate.py --base "base_conhecimento"
```

## Critero de Sucesso (Amanha)
- Markdown gerado com ruido reduzido e sinais tecnicos corretos
- OCR gera poucos arquivos, mas com alto valor
- BK validator identifica problemas reais (nao so formato)
