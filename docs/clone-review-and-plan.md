# Revisao Completa e Plano de Acao

## Visao Geral da Necessidade
Voce quer um agente de cadastro premium para moda masculina 30+ que:
- transforme ficha tecnica em argumento de venda,
- mantenha tom premium discreto,
- reduza devolucao,
- gere SEO consistente,
- use base de conhecimento higienizada e confiavel.

O sistema precisa de dois motores:
1. Motor de conteudo (gera cadastro com estrutura fixa).
2. Motor de conhecimento (BK estruturada com termos tecnicos e beneficios).

## Diagnostico
Pontos criticos atuais:
- Falta estrutura obrigatoria no texto gerado.
- BK ainda nao tem camada RAW -> EXTRAIDO -> MARKDOWN.
- BK Reader nao mede confianca, hits e termos ausentes.
- Nao ha validador de qualidade da BK.
- Coleta de concorrentes exige filtros masculinos e sitemaps alternativos.

## Objetivos Operacionais
- Estrutura fixa no cadastro (headline, abertura, beneficios, autoridade, uso, risco).
- BK com confianca e rastreabilidade.
- Pipeline de ingestao em camadas.
- Validacao minima antes de publicar conhecimento.
- Coleta masculina focada por paths e sitemaps.

## Plano de Acao Implementado
1. Atualizar SPEC com estrutura obrigatoria e campos adicionais.
2. Criar pipeline RAW -> EXTRAIDO -> MARKDOWN.
3. Adicionar BK Reader com confidence_score, hits e missing_terms.
4. Ajustar auditor para penalizar baixa confianca.
5. Criar validador de BK.
6. Criar pacote inicial de BK (tecidos, modelagem, tecnologias).

## Decisoes de Design
- Foco em conteudo masculino (paths e filtros).
- Markdown como memoria oficial.
- Textos com linguagem objetiva, premium discreto.
- Penalizacao automatica quando BK estiver fraca.
